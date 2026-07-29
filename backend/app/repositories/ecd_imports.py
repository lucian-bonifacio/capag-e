from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.repositories.declared_snapshots import Base


class CompanyModel(Base):
    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tax_id: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    ecd_files: Mapped[list[EcdFileModel]] = relationship(back_populates="company")
    analyses: Mapped[list[AnalysisModel]] = relationship(back_populates="company")


class EcdFileModel(Base):
    __tablename__ = "ecd_files"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    original_content: Mapped[bytes | None] = mapped_column(LargeBinary(), nullable=True)
    content_size: Mapped[int | None] = mapped_column(BigInteger(), nullable=True)
    parser_version: Mapped[str | None] = mapped_column(String(40), nullable=True, index=True)
    reprocessed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    preparation_status: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="REIMPORTACAO_NECESSARIA",
        index=True,
    )
    reprocessing_result: Mapped[str | None] = mapped_column(String(40), nullable=True)
    layout: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    period_start: Mapped[date] = mapped_column(Date(), nullable=False)
    period_end: Mapped[date] = mapped_column(Date(), nullable=False)
    imported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    company: Mapped[CompanyModel] = relationship(back_populates="ecd_files")
    analyses: Mapped[list[AnalysisModel]] = relationship(back_populates="ecd_file")


class AnalysisModel(Base):
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    ecd_file_id: Mapped[str] = mapped_column(ForeignKey("ecd_files.id"), nullable=False, index=True)
    methodology_version_id: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    company: Mapped[CompanyModel] = relationship(back_populates="analyses")
    ecd_file: Mapped[EcdFileModel] = relationship(back_populates="analyses")
    exercises: Mapped[list[ExerciseModel]] = relationship(back_populates="analysis")


class ExerciseModel(Base):
    __tablename__ = "analysis_exercises"
    __table_args__ = (UniqueConstraint("analysis_id", "year", name="uq_analysis_exercises_year"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    analysis_id: Mapped[str] = mapped_column(ForeignKey("analyses.id"), nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    methodology_version_id: Mapped[str | None] = mapped_column(String(120), nullable=True)

    analysis: Mapped[AnalysisModel] = relationship(back_populates="exercises")
    accounts_i050: Mapped[list[EcdI050AccountModel]] = relationship(back_populates="exercise")
    reference_links_i051: Mapped[list[EcdI051ReferenceLinkModel]] = relationship(
        back_populates="exercise"
    )
    bookkeeping_i010: Mapped[list[EcdI010BookkeepingModel]] = relationship(
        back_populates="exercise"
    )
    book_headers_i030: Mapped[list[EcdI030BookHeaderModel]] = relationship(
        back_populates="exercise"
    )
    aggregation_links_i052: Mapped[list[EcdI052AggregationLinkModel]] = relationship(
        back_populates="exercise"
    )
    balance_periods_i150: Mapped[list[EcdI150BalancePeriodModel]] = relationship(
        back_populates="exercise"
    )
    balances_i155: Mapped[list[EcdI155BalanceModel]] = relationship(back_populates="exercise")
    entries_i200: Mapped[list[EcdI200EntryModel]] = relationship(back_populates="exercise")
    statements_j005: Mapped[list[EcdJ005StatementModel]] = relationship(
        back_populates="exercise"
    )
    j100_rows: Mapped[list[EcdJ100BalanceRowModel]] = relationship(back_populates="exercise")
    j150_presence: Mapped[list[EcdJ150PresenceModel]] = relationship(
        back_populates="exercise"
    )


class EcdI050AccountModel(Base):
    __tablename__ = "ecd_i050_accounts"
    __table_args__ = (UniqueConstraint("exercise_id", "account_code", name="uq_i050_account"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"),
        nullable=False,
        index=True,
    )
    account_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    account_name: Mapped[str] = mapped_column(String(255), nullable=False)
    account_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    account_nature: Mapped[str | None] = mapped_column(String(20), nullable=True)
    level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    parent_account_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line: Mapped[str] = mapped_column(Text(), nullable=False)

    exercise: Mapped[ExerciseModel] = relationship(back_populates="accounts_i050")


class EcdI051ReferenceLinkModel(Base):
    __tablename__ = "ecd_i051_reference_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"),
        nullable=False,
        index=True,
    )
    account_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    reference_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line: Mapped[str] = mapped_column(Text(), nullable=False)

    exercise: Mapped[ExerciseModel] = relationship(back_populates="reference_links_i051")


class EcdI010BookkeepingModel(Base):
    __tablename__ = "ecd_i010_bookkeeping"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"),
        nullable=False,
        index=True,
    )
    bookkeeping_form: Mapped[str] = mapped_column(String(1), nullable=False)
    bookkeeping_version: Mapped[str | None] = mapped_column(String(40), nullable=True)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line: Mapped[str] = mapped_column(Text(), nullable=False)

    exercise: Mapped[ExerciseModel] = relationship(back_populates="bookkeeping_i010")


class EcdI030BookHeaderModel(Base):
    __tablename__ = "ecd_i030_book_headers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"),
        nullable=False,
        index=True,
    )
    closing_date: Mapped[date] = mapped_column(Date(), nullable=False)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line: Mapped[str] = mapped_column(Text(), nullable=False)

    exercise: Mapped[ExerciseModel] = relationship(back_populates="book_headers_i030")


class EcdI052AggregationLinkModel(Base):
    __tablename__ = "ecd_i052_aggregation_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"),
        nullable=False,
        index=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("ecd_i050_accounts.id"),
        nullable=False,
        index=True,
    )
    account_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    cost_center_code: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    aggregation_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line: Mapped[str] = mapped_column(Text(), nullable=False)

    exercise: Mapped[ExerciseModel] = relationship(back_populates="aggregation_links_i052")
    account: Mapped[EcdI050AccountModel] = relationship()


class EcdI150BalancePeriodModel(Base):
    __tablename__ = "ecd_i150_balance_periods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"),
        nullable=False,
        index=True,
    )
    period_start: Mapped[date] = mapped_column(Date(), nullable=False)
    period_end: Mapped[date] = mapped_column(Date(), nullable=False)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line: Mapped[str] = mapped_column(Text(), nullable=False)

    exercise: Mapped[ExerciseModel] = relationship(back_populates="balance_periods_i150")
    balances_i155: Mapped[list[EcdI155BalanceModel]] = relationship(
        back_populates="balance_period"
    )


class EcdI155BalanceModel(Base):
    __tablename__ = "ecd_i155_balances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"),
        nullable=False,
        index=True,
    )
    balance_period_id: Mapped[int | None] = mapped_column(
        ForeignKey("ecd_i150_balance_periods.id"),
        nullable=True,
        index=True,
    )
    account_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    cost_center_code: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    initial_balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    initial_balance_indicator: Mapped[str] = mapped_column(String(1), nullable=False)
    debit_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    credit_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    final_balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    final_balance_indicator: Mapped[str] = mapped_column(String(1), nullable=False)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line: Mapped[str] = mapped_column(Text(), nullable=False)

    exercise: Mapped[ExerciseModel] = relationship(back_populates="balances_i155")
    balance_period: Mapped[EcdI150BalancePeriodModel | None] = relationship(
        back_populates="balances_i155"
    )


class EcdI200EntryModel(Base):
    __tablename__ = "ecd_i200_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"),
        nullable=False,
        index=True,
    )
    entry_number: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    entry_date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    total_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line: Mapped[str] = mapped_column(Text(), nullable=False)

    exercise: Mapped[ExerciseModel] = relationship(back_populates="entries_i200")
    items: Mapped[list[EcdI250EntryItemModel]] = relationship(back_populates="entry")


class EcdI250EntryItemModel(Base):
    __tablename__ = "ecd_i250_entry_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("ecd_i200_entries.id"), nullable=False, index=True)
    account_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    counterparty_account_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    debit_credit_indicator: Mapped[str | None] = mapped_column(String(1), nullable=True)
    history: Mapped[str | None] = mapped_column(Text(), nullable=True)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line: Mapped[str] = mapped_column(Text(), nullable=False)

    entry: Mapped[EcdI200EntryModel] = relationship(back_populates="items")


class EcdJ005StatementModel(Base):
    __tablename__ = "ecd_j005_statements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"),
        nullable=False,
        index=True,
    )
    period_start: Mapped[date] = mapped_column(Date(), nullable=False)
    period_end: Mapped[date] = mapped_column(Date(), nullable=False, index=True)
    statement_id: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    statement_header: Mapped[str | None] = mapped_column(Text(), nullable=True)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line: Mapped[str] = mapped_column(Text(), nullable=False)

    exercise: Mapped[ExerciseModel] = relationship(back_populates="statements_j005")
    j100_rows: Mapped[list[EcdJ100BalanceRowModel]] = relationship(
        back_populates="statement"
    )
    j150_presence: Mapped[list[EcdJ150PresenceModel]] = relationship(
        back_populates="statement"
    )


class EcdJ100BalanceRowModel(Base):
    __tablename__ = "ecd_j100_balance_rows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"),
        nullable=False,
        index=True,
    )
    statement_id: Mapped[int | None] = mapped_column(
        ForeignKey("ecd_j005_statements.id"),
        nullable=True,
        index=True,
    )
    aggregation_code: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    aggregation_code_type: Mapped[str | None] = mapped_column(String(1), nullable=True)
    aggregation_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    parent_aggregation_code: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        index=True,
    )
    balance_group: Mapped[str | None] = mapped_column(String(1), nullable=True, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    initial_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    initial_debit_credit_indicator: Mapped[str | None] = mapped_column(
        String(1),
        nullable=True,
    )
    final_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    final_debit_credit_indicator: Mapped[str | None] = mapped_column(String(1), nullable=True)
    explanatory_note_reference: Mapped[str | None] = mapped_column(Text(), nullable=True)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line: Mapped[str] = mapped_column(Text(), nullable=False)

    exercise: Mapped[ExerciseModel] = relationship(back_populates="j100_rows")
    statement: Mapped[EcdJ005StatementModel | None] = relationship(
        back_populates="j100_rows"
    )


class EcdJ150PresenceModel(Base):
    __tablename__ = "ecd_j150_presence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_exercises.id"),
        nullable=False,
        index=True,
    )
    statement_id: Mapped[int | None] = mapped_column(
        ForeignKey("ecd_j005_statements.id"),
        nullable=True,
        index=True,
    )
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line: Mapped[str] = mapped_column(Text(), nullable=False)

    exercise: Mapped[ExerciseModel] = relationship(back_populates="j150_presence")
    statement: Mapped[EcdJ005StatementModel | None] = relationship(
        back_populates="j150_presence"
    )
