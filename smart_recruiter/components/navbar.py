import reflex as rx

def navbar() -> rx.Component:
    return rx.box(
        rx.container(
            rx.hstack(
                # logo
                rx.hstack(
                    rx.icon('brain-circuit', size=20, color='#6366f1'),
                    rx.heading('SmarRecruiter', size='5', weight='bold', color='white'),
                    rx.badge('v1.0', variant='soft', color_scheme='indigo'),
                    align='center',
                    spacing='3'
                ),
                rx.spacer(),

                # menu
                rx.hstack(
                    rx.link('Dashboard', href='#', color='white', weight='medium', text_decoration='none'),
                    rx.link('History', href='#', color='gray', weight='medium', _hover={'color': 'white'}),
                    rx.link('Setting', href='#', color='gray', weight='medium', _hover={'color': 'white'}),

                    rx.divider(orientation='vertical', height='20px', color_scheme='gray'),

                    rx.hstack(
                        rx.text('Admin', size='2', color='gray', display=['none', 'none', 'block']),
                        rx.avatar(fallback='BD', size='3', radius='full', color_scheme='indigo', variant='solid'),
                        align='center',
                        spacing='3'
                    ),
                    spacing='6',
                    align='center'
                ),
                width='100%',
                align='center',
            ),
            # container setting: max width ultrawide
            max_width='1200px',
            padding_y='1em',
        ),
        
        # styling navbar
        position='sticky',
        top='0',
        z_index='999',
        # padding_x='2em',
        # padding_y='1.2em',
        width='100%',
        # efek glassmorphism dark mode
        background='rgba(9, 9, 11, 0.8)',
        backdrop_filter='blur(10px)',
        border_bottom='1px solid rgba(255, 255, 255, 0.08)'
    )