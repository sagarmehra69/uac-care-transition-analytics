def build_executive_summary(
    start_date,
    end_date,
    summary,
    bn_sum,
    safe_pct
):

    return f'''
**Period:** {start_date} to {end_date}

**KPIs:** 
Transfer Efficiency: {safe_pct(summary.get('avg_transfer_eff'))}

Discharge Effectiveness:
{safe_pct(summary.get('avg_discharge_eff'), 2)}

Throughput:
{safe_pct(summary.get('avg_throughput'))}

**Backlog:** 
Current: {summary.get('current_backlog', 0):,}

Peak:
{summary.get('peak_backlog', 0):,}

on {summary.get('peak_backlog_date', 'N/A')}

**Bottlenecks:** 
CBP: {bn_sum.get('pct_cbp_bottleneck', 0):.1f}%

HHS: {bn_sum.get('pct_hhs_bottleneck', 0):.1f}%

Sustained:
{bn_sum.get('n_sustained_periods', 0):,} days

Critical Alerts:
{bn_sum.get('n_critical_alerts', 0):,}
'''