"""
Advanced Enterprise Dashboard - Showcase of Declarative Streamlit Features

This example demonstrates ALL major features of the library:
1. Component-based architecture with effects
2. Container management (columns, expanders, tabs)
3. Session state management
4. Error handling per component
5. Event-driven architecture with Topics and Broker
6. Fragments for partial updates
7. Dialogs for user interactions
8. Stateful components
9. Reactive effects system
10. Serialization capabilities
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from json import dumps

# Import all necessary components from the library
from declarative_streamlit.base.app.singleapp import AppPage
from declarative_streamlit.base.app.fragment import AppFragment
from declarative_streamlit.base.app.dialog import AppDialog
from declarative_streamlit.base.logic import SessionState
from declarative_streamlit.config.common.stdstreamlit import StreamlitCommonStandard
from declarative_streamlit.core.logic.topic import BaseTopic
from declarative_streamlit.core.logic.broker import BaseBroker

# ============================================================================
# CONFIGURATION & INITIALIZATION
# ============================================================================

AppPage.set_page_config(
    layout="wide",
    page_icon="📊",
    title="Advanced Enterprise Dashboard"
)

app = AppPage(standard=StreamlitCommonStandard())

# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

# Create session states for different parts of the application
selected_department = SessionState("department", initial_value="Sales")
date_range = SessionState("date_range", initial_value=7)
refresh_count = SessionState("refresh_count", initial_value=0)
notification_count = SessionState("notifications", initial_value=0)
alert_messages = SessionState("alerts", initial_value=[])
filter_active = SessionState("filter_active", initial_value=True)
realtime_data = SessionState("realtime_data", initial_value=[])

# ============================================================================
# EVENT-DRIVEN ARCHITECTURE: TOPICS & BROKER
# ============================================================================

# Create a broker for managing all events
event_broker = BaseBroker(name="dashboard_broker", debug=False)

# Topic 1: Data refresh events
class DataRefreshTopic(BaseTopic):
    """Handles all data refresh operations"""
    pass

data_refresh_topic = DataRefreshTopic("data_refresh", broker=event_broker, debug=False)

@data_refresh_topic.register(priority=1, transactional=True)
def refresh_handler(message):
    """Handle data refresh events"""
    refresh_count.set_value(refresh_count.value + 1)
    st.toast(f"🔄 Data refreshed! Count: {refresh_count.value}", icon="✅")

@data_refresh_topic.register(priority=2)
def log_refresh_handler(message):
    """Log refresh events"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    alerts = alert_messages.value
    alerts.append(f"[{timestamp}] Data refresh triggered by {message.get('sender', 'unknown')}")
    if len(alerts) > 5:
        alerts = alerts[-5:]  # Keep only last 5 alerts
    alert_messages.set_value(alerts)

# Topic 2: Notification events
class NotificationTopic(BaseTopic):
    """Handles notification events"""
    pass

notification_topic = NotificationTopic("notifications", broker=event_broker, debug=False)

@notification_topic.register(priority=1)
def notification_handler(message):
    """Handle notification events"""
    notification_count.set_value(notification_count.value + 1)
    msg_type = message.get("message_type", "info")
    data = message.get("data", "")
    
    if msg_type == "success":
        st.success(data)
    elif msg_type == "warning":
        st.warning(data)
    elif msg_type == "error":
        st.error(data)
    else:
        st.info(data)

@notification_topic.register(priority=0, generic=True)
def generic_notification_logger(message):
    """Log all notifications"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    alerts = alert_messages.value
    alerts.append(f"[{timestamp}] Notification: {message.get('data', 'N/A')}")
    if len(alerts) > 10:
        alerts = alerts[-10:]
    alert_messages.set_value(alerts)

# Register topics with broker
event_broker.subscribe(data_refresh_topic)
event_broker.subscribe(notification_topic)

# Create sender closures for easy event publishing
data_refresh_topic._broker = event_broker
notification_topic._broker = event_broker

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_sales_data(department: str, days: int = 7):
    """Generate sample sales data"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    base_values = {
        "Sales": 1000,
        "Marketing": 800,
        "Engineering": 1200,
        "Support": 600,
        "HR": 400
    }
    
    base = base_values.get(department, 1000)
    
    data = pd.DataFrame({
        'Date': dates,
        'Revenue': np.random.randint(base, base * 2, days),
        'Expenses': np.random.randint(base // 2, base, days),
        'Customers': np.random.randint(50, 200, days),
        'Conversions': np.random.randint(10, 100, days)
    })
    data['Profit'] = data['Revenue'] - data['Expenses']
    return data

def generate_kpi_data(department: str):
    """Generate KPI metrics"""
    base_values = {
        "Sales": {"revenue": 125000, "growth": 15.3, "target": 150000},
        "Marketing": {"revenue": 85000, "growth": 22.1, "target": 100000},
        "Engineering": {"revenue": 200000, "growth": 8.7, "target": 220000},
        "Support": {"revenue": 45000, "growth": 12.5, "target": 50000},
        "HR": {"revenue": 30000, "growth": 5.2, "target": 35000}
    }
    return base_values.get(department, base_values["Sales"])

def generate_team_data(department: str):
    """Generate team performance data"""
    team_sizes = {
        "Sales": 15,
        "Marketing": 12,
        "Engineering": 25,
        "Support": 10,
        "HR": 8
    }
    
    size = team_sizes.get(department, 10)
    
    return pd.DataFrame({
        'Employee': [f"Employee {i+1}" for i in range(size)],
        'Performance': np.random.randint(60, 100, size),
        'Tasks Completed': np.random.randint(10, 50, size),
        'Rating': np.random.uniform(3.5, 5.0, size).round(1)
    })

# ============================================================================
# DIALOGS
# ============================================================================

# Dialog 1: Settings Dialog
settings_dialog = AppDialog(
    title="⚙️ Dashboard Settings",
    width="large",
    standard=StreamlitCommonStandard()
)

settings_dialog.add_component(st.subheader, "Configure Dashboard Preferences")

settings_dialog.add_component(
    st.slider,
    "Auto-refresh interval (seconds):",
    min_value=5,
    max_value=60,
    value=30,
    key="refresh_interval_setting"
).add_effect(
    lambda val: st.info(f"Refresh interval set to {val} seconds")
)

settings_dialog.add_component(
    st.checkbox,
    "Enable notifications",
    value=True,
    key="enable_notifications"
).add_effect(
    lambda val: notification_topic.publish_event({
        "sender": "settings",
        "data": f"Notifications {'enabled' if val else 'disabled'}",
        "message_type": "info"
    })
)

settings_dialog.add_component(
    st.selectbox,
    "Chart theme:",
    options=["Default", "Dark", "Light", "Colorful"],
    key="chart_theme"
).add_effect(
    lambda val: st.success(f"Theme changed to: {val}")
)

settings_dialog.add_component(
    st.button,
    "Save Settings",
    key="save_settings_btn",
    type="primary"
).add_effect(
    lambda *_: st.success("✅ Settings saved successfully!")
)

# Dialog 2: Export Dialog
export_dialog = AppDialog(
    title="📥 Export Data",
    width="small",
    standard=StreamlitCommonStandard()
)

export_dialog.add_component(st.write, "Select export format:")

export_dialog.add_component(
    st.radio,
    "Format:",
    options=["CSV", "Excel", "JSON", "PDF"],
    key="export_format"
).add_effect(
    lambda val: st.info(f"Selected format: {val}")
)

export_dialog.add_component(
    st.button,
    "Export Now",
    key="export_btn",
    type="primary"
).add_effect(
    lambda *_: notification_topic.publish_event({
        "sender": "export_dialog",
        "data": "📊 Data exported successfully!",
        "message_type": "success"
    })
)

# ============================================================================
# HEADER SECTION
# ============================================================================

app.add_component(st.title, "📊 Advanced Enterprise Dashboard")

app.add_component(
    st.markdown,
    """
    <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
        <b>🚀 Showcase of Declarative Streamlit Features:</b> 
        Component Architecture • Event-Driven Logic • Reactive Effects • State Management • Error Handling
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================================
# CONTROL PANEL (Top Row with Tabs)
# ============================================================================

with app.add_container(st.columns, [3, 1, 1, 1]) as control_panel:
    control_panel.set_column_based(True)
    
    # Column 1: Department selector
    control_panel.add_component(
        st.selectbox,
        "🏢 Select Department:",
        options=["Sales", "Marketing", "Engineering", "Support", "HR"],
        key="department_selector"
    ).add_effect(
        lambda val: selected_department.set_value(val)
    ).add_effect(
        lambda val: notification_topic.publish_event({
            "sender": "department_selector",
            "data": f"Switched to {val} department",
            "message_type": "info"
        })
    ).set_stateful(True)
    
    # Column 2: Date range selector
    control_panel.add_component(
        st.selectbox,
        "📅 Time Range:",
        options=[7, 14, 30, 90],
        format_func=lambda x: f"Last {x} days",
        key="date_range_selector"
    ).add_effect(
        lambda val: date_range.set_value(val)
    ).set_stateful(True)
    
    # Column 3: Refresh button
    control_panel.add_component(
        st.button,
        "🔄 Refresh",
        key="refresh_btn",
        use_container_width=True,
        type="primary"
    ).add_effect(
        lambda *_: data_refresh_topic.publish_event({
            "sender": "refresh_button",
            "data": "Manual refresh triggered",
            "destination": "refresh_handler",
            "message_type": "refresh"
        })
    ).set_stateful(True).set_errhandler(
        lambda e: st.error(f"Refresh failed: {e}")
    )
    
    # Column 4: Settings button
    control_panel.add_component(
        st.button,
        "⚙️ Settings",
        key="settings_btn",
        use_container_width=True
    ).add_effect(
        settings_dialog
    ).set_stateful(True)

# ============================================================================
# KPI METRICS ROW
# ============================================================================

app.add_component(st.markdown, "---")
app.add_component(st.subheader, "📈 Key Performance Indicators")

with app.add_container(st.columns, 4) as kpi_row:
    kpi_row.set_column_based(True)
    
    # Dynamic KPI calculation based on selected department
    def show_revenue_kpi():
        kpi = generate_kpi_data(selected_department.value)
        st.metric(
            label="💰 Revenue",
            value=f"${kpi['revenue']:,.0f}",
            delta=f"{kpi['growth']}%"
        )
    
    def show_target_kpi():
        kpi = generate_kpi_data(selected_department.value)
        progress = (kpi['revenue'] / kpi['target']) * 100
        st.metric(
            label="🎯 Target Progress",
            value=f"{progress:.1f}%",
            delta=f"${kpi['target'] - kpi['revenue']:,.0f} to go"
        )
    
    def show_notifications_kpi():
        st.metric(
            label="🔔 Notifications",
            value=notification_count.value,
            delta=f"{refresh_count.value} refreshes"
        )
    
    def show_status_kpi():
        status = "🟢 Active" if filter_active.value else "🔴 Inactive"
        st.metric(
            label="📊 System Status",
            value=status,
            delta="All systems operational"
        )
    
    # Add KPIs with error handling
    kpi_row.add_component(show_revenue_kpi).set_errhandler(
        lambda e: st.error("Revenue calculation error")
    ).set_fatal(False)
    
    kpi_row.add_component(show_target_kpi).set_errhandler(
        lambda e: st.error("Target calculation error")
    ).set_fatal(False)
    
    kpi_row.add_component(show_notifications_kpi).set_errhandler(
        lambda e: st.error("Notification count error")
    ).set_fatal(False)
    
    kpi_row.add_component(show_status_kpi).set_errhandler(
        lambda e: st.error("Status display error")
    ).set_fatal(False)

# ============================================================================
# MAIN CONTENT AREA WITH TABS
# ============================================================================

app.add_component(st.markdown, "---")

with app.add_container(st.tabs, ["📊 Analytics", "👥 Team Performance", "📈 Trends", "🔔 Activity Log"]) as tabs:
    tabs.set_column_based(True)
    
    # ========================================================================
    # TAB 1: ANALYTICS
    # ========================================================================
    
    def render_analytics_tab():
        st.subheader("Revenue & Expense Analysis")
        
        # Generate data based on current selections
        data = generate_sales_data(selected_department.value, date_range.value)
        
        # Two-column layout for charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📈 Revenue vs Expenses**")
            chart_data = data[['Date', 'Revenue', 'Expenses']].set_index('Date')
            st.line_chart(chart_data)
        
        with col2:
            st.markdown("**💰 Profit Trend**")
            profit_data = data[['Date', 'Profit']].set_index('Date')
            st.area_chart(profit_data)
        
        # Expandable detailed data
        with st.expander("📋 View Detailed Data"):
            st.dataframe(
                data.style.highlight_max(axis=0, color='lightgreen'),
                use_container_width=True
            )
            
            # Export button
            csv = data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{selected_department.value}_data.csv",
                mime="text/csv"
            )
    
    tabs.add_component(render_analytics_tab).set_errhandler(
        lambda e: st.error(f"Analytics rendering error: {e}")
    ).set_fatal(False)
    
    # ========================================================================
    # TAB 2: TEAM PERFORMANCE
    # ========================================================================
    
    def render_team_tab():
        st.subheader("Team Performance Overview")
        
        team_data = generate_team_data(selected_department.value)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**📊 Performance Distribution**")
            st.bar_chart(team_data.set_index('Employee')['Performance'])
        
        with col2:
            st.markdown("**⭐ Top Performers**")
            top_performers = team_data.nlargest(5, 'Performance')
            for idx, row in top_performers.iterrows():
                st.write(f"**{row['Employee']}**: {row['Performance']}% ({row['Rating']}⭐)")
        
        st.markdown("**👥 Complete Team Data**")
        st.dataframe(team_data, use_container_width=True)
    
    tabs.add_component(render_team_tab).set_errhandler(
        lambda e: st.error(f"Team data rendering error: {e}")
    ).set_fatal(False)
    
    # ========================================================================
    # TAB 3: TRENDS
    # ========================================================================
    
    def render_trends_tab():
        st.subheader("Customer & Conversion Trends")
        
        data = generate_sales_data(selected_department.value, date_range.value)
        
        # Multi-metric chart
        st.markdown("**📊 Customer Acquisition & Conversions**")
        trend_data = data[['Date', 'Customers', 'Conversions']].set_index('Date')
        st.line_chart(trend_data)
        
        # Conversion rate calculation
        data['Conversion_Rate'] = (data['Conversions'] / data['Customers'] * 100).round(2)
        
        st.markdown("**🎯 Conversion Rate Analysis**")
        st.bar_chart(data.set_index('Date')['Conversion_Rate'])
        
        # Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Conversion Rate", f"{data['Conversion_Rate'].mean():.2f}%")
        with col2:
            st.metric("Total Customers", f"{data['Customers'].sum():,}")
        with col3:
            st.metric("Total Conversions", f"{data['Conversions'].sum():,}")
    
    tabs.add_component(render_trends_tab).set_errhandler(
        lambda e: st.error(f"Trends rendering error: {e}")
    ).set_fatal(False)
    
    # ========================================================================
    # TAB 4: ACTIVITY LOG
    # ========================================================================
    
    def render_activity_log():
        st.subheader("🔔 Recent Activity")
        
        if alert_messages.value:
            for alert in reversed(alert_messages.value):
                st.text(alert)
        else:
            st.info("No recent activity")
        
        if st.button("Clear Log", key="clear_log_btn"):
            alert_messages.set_value([])
            st.rerun()
    
    tabs.add_component(render_activity_log).set_errhandler(
        lambda e: st.error(f"Activity log error: {e}")
    ).set_fatal(False)

# ============================================================================
# REAL-TIME FRAGMENT (Auto-updating section)
# ============================================================================

app.add_component(st.markdown, "---")
app.add_component(st.subheader, "⚡ Real-Time Monitor (Auto-updates every 10s)")

# Create a fragment that updates every 10 seconds
realtime_fragment = AppFragment(run_every="10s", standard=StreamlitCommonStandard())

def update_realtime_data():
    """Update real-time data"""
    current_time = datetime.now().strftime("%H:%M:%S")
    value = np.random.randint(50, 150)
    
    data = realtime_data.value
    data.append({"time": current_time, "value": value})
    
    # Keep only last 10 entries
    if len(data) > 10:
        data = data[-10:]
    
    realtime_data.set_value(data)

realtime_fragment.add_function(update_realtime_data)

def show_realtime_chart():
    if realtime_data.value:
        df = pd.DataFrame(realtime_data.value)
        st.line_chart(df.set_index('time')['value'])
        st.caption(f"Last update: {datetime.now().strftime('%H:%M:%S')}")
    else:
        st.info("Waiting for data...")

realtime_fragment.add_component(show_realtime_chart)

# Add the fragment to the app
app.add_fragment(realtime_fragment)

# ============================================================================
# INTERACTIVE CONTROLS SECTION
# ============================================================================

app.add_component(st.markdown, "---")
app.add_component(st.subheader, "🎮 Interactive Controls")

with app.add_container(st.columns, 3) as controls:
    controls.set_column_based(True)
    
    # Control 1: Toggle filter
    controls.add_component(
        st.toggle,
        "Enable Data Filtering",
        value=True,
        key="filter_toggle"
    ).add_effect(
        lambda val: filter_active.set_value(val)
    ).add_effect(
        lambda val: notification_topic.publish_event({
            "sender": "filter_toggle",
            "data": f"Data filtering {'enabled' if val else 'disabled'}",
            "message_type": "info"
        })
    ).set_stateful(True)
    
    # Control 2: Send test notification
    controls.add_component(
        st.button,
        "🔔 Send Test Notification",
        key="test_notification_btn",
        use_container_width=True
    ).add_effect(
        lambda *_: notification_topic.publish_event({
            "sender": "test_button",
            "data": "This is a test notification!",
            "destination": "notification_handler",
            "message_type": "info"
        })
    ).set_stateful(True)
    
    # Control 3: Export dialog trigger
    controls.add_component(
        st.button,
        "📥 Export Data",
        key="export_trigger_btn",
        use_container_width=True
    ).add_effect(
        export_dialog
    ).set_stateful(True)

# ============================================================================
# FOOTER WITH SERIALIZATION
# ============================================================================

app.add_component(st.markdown, "---")

with app.add_container(st.expander, "🔧 Advanced: App Serialization & Debug Info") as debug_section:
    
    def show_serialization():
        st.markdown("**📦 Serialized Application Structure**")
        st.caption("This shows the complete component tree in JSON format")
        
        serialized = app.serialize()
        st.json(serialized)
        
        # Download button for serialized app
        st.download_button(
            label="💾 Download App Structure",
            data=dumps(serialized, indent=2),
            file_name="dashboard_structure.json",
            mime="application/json"
        )
    
    debug_section.add_component(show_serialization).set_errhandler(
        lambda e: st.error(f"Serialization error: {e}")
    ).set_fatal(False)
    
    def show_stats():
        st.markdown("**📊 Application Statistics**")
        stats = {
            "Total Refreshes": refresh_count.value,
            "Total Notifications": notification_count.value,
            "Current Department": selected_department.value,
            "Date Range": f"Last {date_range.value} days",
            "Filter Active": filter_active.value,
            "Events in Log": len(alert_messages.value)
        }
        st.json(stats)
    
    debug_section.add_component(show_stats)

# ============================================================================
# START THE APPLICATION
# ============================================================================

app.start()
