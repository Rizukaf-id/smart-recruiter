import reflex as rx
from ..models import CandidateReview

def score_circle(score: int) -> rx.Component:
    '''Circular Progress Bar Score'''
    base_color = rx.cond(score >= 75, 'grass', rx.cond(score >=50, 'amber', 'tomato'))

    return rx.center(
        rx.text(
            f'{score}',
            weight='bold',
            size='5',
            color=rx.color(base_color, 11)
        ),
        width='70px',
        height='70px',
        border_radius='full',
        border='5px solid',
        border_color=rx.color(base_color, 9),
        background=rx.color(base_color, 3),
        box_shadow='0 0 10px -2px rgba(0,0,0,0.5)'
    )

def candidate_card(review: CandidateReview) -> rx.Component:
    '''Tampilan kartu kandidat'''
    return rx.card(
        rx.vstack(
            rx.hstack(
                # avatar dan info utama
                rx.avatar(
                    fallback=review.candidate_name.to(str)[:2],
                    size='5',
                    radius='full',
                    color_scheme='indigo',
                ),
                rx.vstack(
                    rx.text(review.candidate_name, weight='bold', size='4', color='white'),
                    rx.text(review.filename, size='1', color='gray'),
                    spacing='1',
                    align_items='start'
                ),
                rx.spacer(),
                # score badge
                score_circle(review.score),
                width='100%',
                align='center',
            ),

            rx.divider(margin_y='1em', opacity=0.3),

            # summary
            rx.text(review.summary, size='2', color='gray', line_height='1.6em'),

            # grid pros cons
            rx.grid(
                rx.box(
                    rx.badge('STRENGTHS', color_scheme='grass', variant='surface', margin_bottom='0.5em'),
                    rx.foreach(review.pros, lambda p: rx.text(f'• {p}', size='1', color='#a1a1aa')),
                    padding='1em',
                    background='rgba(46, 204, 113, 0.05)',
                    border_radius='8px',
                    height='100%'
                ),
                rx.box(
                    rx.badge('RED FLAGS', color_scheme='tomato', variant='surface', margin_bottom='0.5em'),
                    rx.foreach(review.cons, lambda c: rx.text(f'• {c}', size='1', color='lightgray')),
                    padding='1em',
                    background='rgba(239, 68, 68, 0.05)',
                    border_radius='8px',
                    height='100%'
                ),
                columns='2',
                spacing='4',
                width='100%',
                margin_top='1em'
            ),
            width='100%',
            spacing='4'
        ),
        variant='surface',
        width='100%',
        background='linear-gradient(145deg, #1e1e24 0%, #1a1a20 100%)',
        border='1px solid #27272a',
        padding='1.5em',
        _hover={'border_color': '#6366f1', 'transition': '0.3s'},
    )