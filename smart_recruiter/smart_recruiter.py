import reflex as rx
from .state import AppState
from .components.result_card import candidate_card
from .components.navbar import navbar

def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                # header section
                rx.vstack(
                    rx.heading(
                        'Smart Recruiter AI',
                        size='9',
                        weight='bold',
                        text_align='center',
                        background_image='linear-gradient(45deg, #4f46e5, #ec4899)',
                        background_clip='text',
                        color='transparent',
                    ),
                    rx.text(
                        'Upload CV PDF. Biarkan AI melakukan screening',
                        size='4',
                        color='gray',
                        weight='medium'
                    ),
                    spacing='2',
                    align='center',
                    margin_bottom='3em',
                    margin_top='2em'
                ),
                rx.card(
                    rx.vstack(
                        # label 1
                        rx.hstack(
                            rx.icon('file-text', size=20, color='#a855f7'),
                            rx.text('1. Job Description (JD)', weight='bold', color='white'),
                            align='center',
                            spacing='2',
                            width='100%'
                        ),
                        rx.text_area(
                            placeholder='Paste deskripsi pekerjaan lengakp di sini...',
                            value=AppState.jd_text,
                            on_change=AppState.set_jd_text,
                            min_height='180px',
                            variant='surface',
                            radius='large',
                            size='3',
                            color_scheme='gray',
                            width='100%',
                            background='rgba(255, 255, 255, 0.05)',
                            border='1px solid rgba(255, 255, 255, 0.1)',
                            _focus={'border_color': '#a855f7', 'outline': 'none'}
                        ),

                        rx.separator(size='4', color_scheme='gray', opacity=0.3),

                        
                        # label 2
                        rx.hstack(
                            rx.icon('upload-cloud', size=20, color='#ec4899'),
                            rx.text('2. Upload Resume (PDF)', weight='bold', color='white'),
                            align='center',
                            spacing='2',
                            width='100%'
                        ),

                        rx.upload(
                            rx.vstack(
                                rx.icon('cloud-upload', size=40, color='#6366f1'),
                                rx.text('Drag & drop CV PDF di sini', weight='bold', size='3'),
                                rx.text('Support multiple files', size='1', color='gray'),
                                align='center',
                                spacing='2'
                            ),
                            id='cv_upload',
                            multiple=True,
                            accept={'application/pdf': ['.pdf']},
                            on_drop=AppState.handle_drop,
                            border='2px dashed rgba(255,255,255, 0.2)',
                            padding='3em',
                            width='100%',
                            background='rgba(99, 102, 241, 0.05)',
                            _hover={'background': 'rgba(99, 102, 241, 0.1', 'border_color': '#6366f1'},
                            border_radius='1em'
                        ),
                        # file preview
                        rx.cond(
                            AppState.uploaded_files,
                            rx.vstack(
                                rx.hstack(
                                    rx.text('File Ready:', color='gray', size='2'),
                                    rx.spacer(),
                                    rx.button('Clear', size='1', variant='ghost',color_scheme='red', on_click=AppState.clear_uploads),
                                ),
                                # loop list nama file
                                rx.foreach(
                                    AppState.uploaded_files,
                                    lambda name: rx.hstack(
                                        rx.hstack(
                                            rx.icon('file-text', size=18, color='#6366f1'),
                                            rx.text(name, size='2', color='white'),
                                            align='center',
                                            spacing='2',
                                        ),
                                        rx.spacer(),
                                        rx.icon_button(
                                            'trash-2',
                                            on_click=AppState.remove_file(name),
                                            size='1',
                                            variant='ghost',
                                            color_scheme='gray',
                                            _hover={'color': '#ef4444', 'background': 'rgba(239, 68, 68, 0.1)'}
                                        ),
                                        width='100%',
                                        padding='0.75em',
                                        background='rgba(255,255,255,0.03)',
                                        border_radius='8px',
                                        align='center',
                                    )
                                ),
                                width='100%',
                                spacing='2',
                                max_height='200px',
                                overflow_y='auto',
                            )
                        ),

                        # button action
                        rx.button(
                            rx.cond(
                                AppState.is_loading,
                                rx.hstack(rx.spinner(size='2'), rx.text('Sedang menganalisis---')),
                                rx.hstack(rx.icon('sparkles'), rx.text('Mulai Screening CV'))
                            ),
                            on_click=AppState.start_analysis,
                            disabled=AppState.is_loading,
                            width='100%',
                            size='4',
                            radius='full',
                            background='linear-gradient(90deg, #4f46e5, #ec4899)',
                            box_shadow='0 4px 20px rgba(99, 102, 241, 0.4)',
                            _hover={'opacity': 0.9, 'transform': 'scale(1.02)'},
                            cursor='pointer',
                            margin_top='1em'
                        ),
                        spacing='5',
                        width='100%'
                    ),
                    width='100%',
                    max_width='700px',
                    padding='2em',
                    background='#18181b',
                    border='1px solid #27272a',
                    box_shadow='0 25px 50px -12px rgba(0, 0, 0, 0.5)'
                ),

                rx.divider(margin_y='4em', opacity=0.2),

                # results


                rx.cond(
                    AppState.results,
                    rx.vstack(
                        rx.hstack(
                            rx.heading('Analyze Results', size='6', color='white'),
                            rx.badge(f'Total: {AppState.results.length()} candidates', variant='soft', color_scheme='indigo'),
                            width='100%',
                            justify='between',
                            align='center',
                            max_width='800px'
                        ),
                        rx.grid(
                            rx.foreach(AppState.results, candidate_card),
                            columns=rx.breakpoints(initial='1', sm='2'),
                            spacing='4',
                            width='100%',
                            max_width='800px'
                        ),
                        # empty state
                        # rx.center(
                        #     rx.vstack(
                        #         rx.icon('file-search', size=50, color='#333'),
                        #         rx.text('Belum ada hasil', color='gray'),
                        #         spacing='2',
                        #         opacity=0.5
                        #     ),
                        #     padding='4em',
                        #     width='100%',
                        #     border='1px dashed #333',
                        #     border_radius='lg'
                        # )
                    )
                    
                ),
                padding_bottom='5em',
                width='100%',
                align='center',
            ),
            padding_x='1em',
        ),
        min_height='100vh',
        background='#09090b',
        font_family='Inter',
    )

# setup theme dark mode
app = rx.App(
    theme=rx.theme(
        appearance='dark',
        accent_color='indigo',
        radius='large',
        has_background=True
    )
)

app.add_page(index, title='Smart Recruiter AI')