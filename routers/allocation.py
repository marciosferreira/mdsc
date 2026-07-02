from fastapi import APIRouter

from allocation_db import get_allocation_db

router = APIRouter(tags=["allocation"])

_ALLOC_SUM = "(allocation_W1 + allocation_W2 + allocation_W3 + allocation_W4 + allocation_W5)"


@router.get("/summary")
def allocation_summary():
    """Resumo simples da alocação KA (quarter atual: month_status done/ongoing)."""
    with get_allocation_db() as conn:
        kpis_row = conn.execute(f"""
            SELECT
                COALESCE(SUM({_ALLOC_SUM}), 0) AS total_alocado,
                COUNT(DISTINCT key_account_code) AS total_kas,
                COUNT(DISTINCT CASE WHEN woi < 10 THEN key_account_code END) AS kas_criticos,
                COUNT(CASE WHEN deal > 0 AND {_ALLOC_SUM} >= deal THEN 1 END) AS deals_completos
            FROM ka_deal_allocation
            WHERE month_status IN ('done', 'ongoing')
        """).fetchone()

        by_ka = conn.execute(f"""
            SELECT
                key_account_code,
                SUM({_ALLOC_SUM}) AS total_alocado,
                AVG(woi) AS woi_medio
            FROM ka_deal_allocation
            WHERE month_status IN ('done', 'ongoing')
            GROUP BY key_account_code
            ORDER BY total_alocado DESC
            LIMIT 10
        """).fetchall()

        woi_bands = conn.execute("""
            SELECT
                CASE
                    WHEN woi < 10 THEN 'Crítico (<10)'
                    WHEN woi < 15 THEN 'Médio (10-15)'
                    ELSE 'Saudável (>=15)'
                END AS band,
                COUNT(*) AS total
            FROM ka_deal_allocation
            WHERE month_status IN ('done', 'ongoing')
            GROUP BY band
        """).fetchall()

    return {
        "kpis": dict(kpis_row),
        "by_key_account": [dict(r) for r in by_ka],
        "woi_bands": [dict(r) for r in woi_bands],
    }
