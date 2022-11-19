"""empty message

Revision ID: a87dba38784f
Revises: fa28855a37d3
Create Date: 2022-11-19 15:32:49.433539

"""
from datetime import datetime,timedelta
from alembic import op
import sqlalchemy as sa
from worker.utils.rates import get_current_exchange_rates,upload_new_data 
from migrations.models.currency import Currency
from migrations.models.exchange_rates import ExchangeRates
from pytz import UTC
from sqlalchemy.exc import IntegrityError
# revision identifiers, used by Alembic.
revision = 'a87dba38784f'
down_revision = 'fa28855a37d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('uq__exchange_rates__id'), 'exchange_rates', ['id'])
    bind = op.get_bind() 
    session = sa.orm.Session(bind=bind)
    for i in range(10):
        today = datetime.now(UTC) - timedelta(days=i)
        for pair in [
            ("USD", "American dollars",),
            ("EUR", "Euro",),
            ("JPY", "Japan Yen",),
            ("CNY", "Chineese Yuan",)
        ]:
            query = sa.insert(Currency).values(
                name=pair[0],
                fullname=pair[1],
                value=1.0
            )
            try:
                session.execute(query)
            except IntegrityError as e:
                session.rollback()
            rates = get_current_exchange_rates([pair[0],], today=today)
            query = sa.insert(ExchangeRates).values(
                code=rates[0].code,
                symbol=rates[0].symbol,
                amount=rates[0].amount,
                rate=rates[0].rate,
                created_at=today
            )
            session.execute(query)
            session.commit()
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq__exchange_rates__id'), 'exchange_rates', type_='unique')
    # ### end Alembic commands ###
