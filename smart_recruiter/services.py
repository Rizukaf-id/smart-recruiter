import os
import asyncio
from typing import List
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.document_loaders import PyPDFLoader
from .models import CandidateReview
from dotenv import load_dotenv
load_dotenv()

class RecruitmentService:
    '''Service Class untuk menangani logika bisnis rekrutmen'''

    def __init__(self):
        self.llm = ChatGroq(
            model='llama-3.3-70b-versatile',
            temperature=0,
            api_key=os.getenv('GROQ_API_KEY')
        )
        self.parser = JsonOutputParser(pydantic_object=CandidateReview)
        self.prompt = ChatPromptTemplate.from_template('''
            Kamu adalah HR Expert. Review kandidat ini berdasarkan JD.
            
            JOB DESCRIPTION:
            {jd}
            
            CV TEXT:
            {cv_text}
            
            Output JSON Only:
            {format_instructions}
        ''')
        self.chain = self.prompt | self.llm | self.parser

    async def _extract_text_from_pdf(self, file_path: str) -> str:
        '''Helper private untuk baca PDF (IO Bound)'''
        try:
            loader = PyPDFLoader(file_path)
            pages = await asyncio.to_thread(loader.load)
            return '\n'.join([p.page_content for p in pages])
        except Exception as e:
            print(f'Error loading PDF {file_path}: {e}')
            return ''
    
    async def _analyze_single_cv(self, file_path: str, filename: str, jd: str) -> CandidateReview:
        '''Proses 1 CV'''
        cv_text = await self._extract_text_from_pdf(file_path)

        if not cv_text:
            return CandidateReview(
                candidate_name='Error Reading File', score=0,
                summary='Gagal ekstrak teks pdf.', filename=filename
            )
        
        try:
            # Panggil LLM (Network Bound)
            result = await self.chain.ainvoke({
                'jd': jd,
                'cv_text': cv_text,
                'format_instructions': self.parser.get_format_instructions()
            })
            # inject filename ke hasil
            result['filename'] = filename
            return CandidateReview(**result)
        except Exception as e:
            return CandidateReview(
                candidate_name='AI Error', score=0,
                saummary=str(e), filename=filename
            )
        
    async def process_batch(self, files_data: list, jd: str) -> List[CandidateReview]:
        '''
        GAME CHANGER: proses banyak CV sekaligus (paralel).
        files_data: list of tuple (path, filename)
        '''
        tasks = []
        for path, name in files_data:
            tasks.append(self._analyze_single_cv(path, name, jd))

        # run paralel
        results = await asyncio.gather(*tasks)
        return results