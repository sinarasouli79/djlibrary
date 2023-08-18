import logging

from celery import shared_task

from library.management.commands.deduct_daily_borrowing_price import Command
from library.management.commands.penalties import Command

logger = logging.getLogger(__name__)


@shared_task
def deduct_dail_borrowing_price_schedule():
    logger.info('deduct daily borrowing price ')
    cmd = Command()
    cmd.handle()
    logger.info('deduct daily borrowing price finished')


@shared_task
def deduct_penalty_price_schedule():
    logger.info('deduct penalty price ')
    cmd = Command()
    cmd.handle()
    logger.info('deduct penalty price finished')
