import reflex as rx
import os
import shutil
from typing import List
from .services import RecruitmentService
from .models import CandidateReview

class AppState(rx.State):
    '''State management untuk aplikasi'''
    jd_text: str = ''
    results: List[CandidateReview] = [] # dict untuk serialization
    uploaded_files: List[str] = []
    is_loading: bool = False
    # processing_progress: int = 0

    # handler saat file didrop (hanya simpan file dan nama)
    async def handle_drop(self, files: list[rx.UploadFile]):
        '''handle drop file'''
        upload_dir = 'temp_uploads'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        for file in files:
            upload_data = await file.read()
            path = os.path.join(upload_dir, file.filename)
            with open(path, 'wb') as f:
                f.write(upload_data)

            if file.filename not in self.uploaded_files:
                self.uploaded_files.append(file.filename)

    async def start_analysis(self):
        '''Mulai proses analisis cv'''
        if not self.jd_text:
            yield rx.window_alert('Job Description tidak boleh kosong!')
            return
        if not self.uploaded_files:
            yield rx.window_alert('Silakan upload minimal 1 file CV!')
            return
        self.is_loading = True
        self.results = []
        yield

        service = RecruitmentService()

        files_to_process = []
        upload_dir = 'temp_uploads'

        for filename in self.uploaded_files:
            path = os.path.join(upload_dir, filename)
            if os.path.exists(path):
                files_to_process.append((path, filename))

        try:
            reviews_objects = await service.process_batch(files_to_process, self.jd_text)
            self.results = reviews_objects
            self.results.sort(key=lambda x: x.score, reverse=True)

        except Exception as e:
            yield rx.window_alert(f'Error during processing: {str(e)}')
        
        finally:
            if os.path.exists(upload_dir):
                shutil.rmtree(upload_dir)
            self.uploaded_files = []
            self.is_loading = False

    def clear_uploads(self):
        self.uploaded_files = []
        upload_dir = 'temp_uploads'
        if os.path.exists(upload_dir):
            shutil.rmtree(upload_dir)
    
    def remove_file(self, filename: str):
        '''Hapus satu file dari list dan dari disk'''

        self.uploaded_files = [f for f in self.uploaded_files if f != filename]

        file_path = os.path.join('temp_uploads', filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f'Error removing file {filename}: {str(e)}')