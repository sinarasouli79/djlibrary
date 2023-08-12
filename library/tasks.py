from celery import shared_task

from library.management.commands.deduct_daily_borrowing_price import Command


@shared_task
def deduct_dail_borrowing_price_schedule():
    cmd = Command()
    cmd.handle()
