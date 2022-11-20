"""empty message

Revision ID: 5de40a7e6fe8
Revises: 
Create Date: 2022-11-19 02:26:38.473289

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5de40a7e6fe8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('role', postgresql.ENUM('DEMO', 'UNVERIFIED', 'REGULAR', 'ADMIN', name='roles'), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('gender', postgresql.ENUM('MALE', 'FEMALE', 'UNSPECIFIED', name='gender'), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('avatar_id', sa.String(), nullable=True),
    sa.Column('birth_date', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__users')),
    sa.UniqueConstraint('email', name=op.f('uq__users__email')),
    sa.UniqueConstraint('id', name=op.f('uq__users__id')),
    sa.UniqueConstraint('username', name=op.f('uq__users__username'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
"""empty message

Revision ID: 7c642e54d680
Revises: 5de40a7e6fe8
Create Date: 2022-11-19 03:38:56.802635

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7c642e54d680'
down_revision = '5de40a7e6fe8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('fullname', sa.String(), nullable=True),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__currency')),
    sa.UniqueConstraint('id', name=op.f('uq__currency__id')),
    sa.UniqueConstraint('name', name=op.f('uq__currency__name'))
    )
    op.create_table('news',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__news')),
    sa.UniqueConstraint('id', name=op.f('uq__news__id'))
    )
    op.create_table('currency_account',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('user_id', postgresql.UUID(), nullable=False),
    sa.Column('currency_id', postgresql.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], name=op.f('fk__currency_account__currency_id__currency'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk__currency_account__user_id__users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__currency_account')),
    sa.UniqueConstraint('id', name=op.f('uq__currency_account__id'))
    )
    op.create_table('transactions',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('currency_account_id', postgresql.UUID(), nullable=False),
    sa.Column('change_value', sa.FLOAT(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['currency_account_id'], ['currency.id'], name=op.f('fk__transactions__currency_account_id__currency'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__transactions')),
    sa.UniqueConstraint('id', name=op.f('uq__transactions__id'))
    )
    op.create_unique_constraint(op.f('uq__users__id'), 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq__users__id'), 'users', type_='unique')
    op.drop_table('transactions')
    op.drop_table('currency_account')
    op.drop_table('news')
    op.drop_table('currency')
    # ### end Alembic commands ###
"""empty message

Revision ID: a0028205d7f2
Revises: c04481b855bd
Create Date: 2022-11-19 10:08:59.270984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0028205d7f2'
down_revision = 'c04481b855bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('currency_account', sa.Column('value', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('currency_account', 'value')
    # ### end Alembic commands ###
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
"""empty message

Revision ID: c04481b855bd
Revises: 7c642e54d680
Create Date: 2022-11-19 08:28:47.687951

"""
from alembic import op
import sqlalchemy as sa
from migrations.models.currency import Currency
from migrations.models.exchange_rates import ExchangeRates 
from datetime import datetime
from pytz import UTC


# revision identifiers, used by Alembic.
revision = 'c04481b855bd'
down_revision = '7c642e54d680'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('uq__currency__id'), 'currency', ['id'])
    op.create_unique_constraint(op.f('uq__currency_account__id'), 'currency_account', ['id'])
    op.create_unique_constraint(op.f('uq__news__id'), 'news', ['id'])
    op.create_unique_constraint(op.f('uq__transactions__id'), 'transactions', ['id'])
    op.add_column('users', sa.Column('phone', sa.String(), nullable=False))
    op.drop_constraint('uq__users__email', 'users', type_='unique')
    op.drop_constraint('uq__users__username', 'users', type_='unique')
    op.create_unique_constraint(op.f('uq__users__phone'), 'users', ['phone'])
    op.drop_column('users', 'email')
    op.drop_column('users', 'username')
    bind = op.get_bind() 
    session = sa.orm.Session(bind=bind)
    today = datetime.now(UTC)
    query = sa.insert(ExchangeRates).values(
        code='1000',
        symbol="RUB",
        amount=1,
        rate=1.0,
        created_at=today
    )
    session.execute(query)
    session.commit()
    query1 = sa.insert(Currency).values(
        name="rub",
        fullname="Rubles",
        value=1.0
    )
    query2 = sa.insert(Currency).values(
        name="usd",
        fullname="American dollars",
        value=60.0
    )
    query3 = sa.insert(Currency).values(
        name="eur",
        fullname="Euro",
        value=60.0
    )
    session.execute(query1)
    session.execute(query2)
    session.execute(query3)
    session.commit()
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(op.f('uq__users__phone'), 'users', type_='unique')
    op.create_unique_constraint('uq__users__username', 'users', ['username'])
    op.create_unique_constraint('uq__users__email', 'users', ['email'])
    op.drop_column('users', 'phone')
    op.drop_constraint(op.f('uq__transactions__id'), 'transactions', type_='unique')
    op.drop_constraint(op.f('uq__news__id'), 'news', type_='unique')
    op.drop_constraint(op.f('uq__currency_account__id'), 'currency_account', type_='unique')
    op.drop_constraint(op.f('uq__currency__id'), 'currency', type_='unique')
    # ### end Alembic commands ###
"""empty message

Revision ID: e0d3a3b30ec0
Revises: a0028205d7f2
Create Date: 2022-11-19 10:30:30.935217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0d3a3b30ec0'
down_revision = 'a0028205d7f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk__transactions__currency_account_id__currency', 'transactions', type_='foreignkey')
    op.create_foreign_key(op.f('fk__transactions__currency_account_id__currency_account'), 'transactions', 'currency_account', ['currency_account_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk__transactions__currency_account_id__currency_account'), 'transactions', type_='foreignkey')
    op.create_foreign_key('fk__transactions__currency_account_id__currency', 'transactions', 'currency', ['currency_account_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
"""empty message

Revision ID: fa28855a37d3
Revises: e0d3a3b30ec0
Create Date: 2022-11-19 15:07:25.461213

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
# revision identifiers, used by Alembic.
revision = 'fa28855a37d3'
down_revision = 'e0d3a3b30ec0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exchange_rates',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('code', sa.INTEGER(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('amount', sa.INTEGER(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__exchange_rates')),
    sa.UniqueConstraint('id', name=op.f('uq__exchange_rates__id'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exchange_rates')
    # ### end Alembic commands ###
