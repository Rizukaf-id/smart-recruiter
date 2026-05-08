import reflex as rx

config = rx.Config(
    app_name="smart_recruiter",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)