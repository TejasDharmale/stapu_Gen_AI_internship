"""
Streamlit UI for GenAI Sports Calendar
Provides interactive dashboard for tournament data with AI insights
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional

# Import local modules
from db_utils import (
    get_all_tournaments, get_tournaments_by_filter, 
    get_tournament_stats, init_database
)
from data_collection import collect_tournaments, TournamentCollector
from export import export_to_csv, export_to_json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="GenAI Sports Calendar",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main Streamlit application"""
    st.title("🏆 GenAI Sports Calendar")
    st.markdown("AI-powered sports tournament management using Hugging Face models")
    
    # Initialize database if needed
    try:
        init_database()
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Filters")
        
        # Sport filter
        sports = ["All"] + ["Cricket", "Football", "Badminton", "Running", "Gym", 
                           "Cycling", "Swimming", "Kabaddi", "Yoga", "Basketball", 
                           "Chess", "Table Tennis"]
        selected_sport = st.selectbox("Select Sport", sports)
        
        # Level filter
        levels = ["All"] + ["Corporate", "School", "College/University", "Club/Academy",
                           "District", "State", "Zonal/Regional", "National", "International"]
        selected_level = st.selectbox("Select Level", levels)
        
        # Date filter
        st.subheader("📅 Date Range")
        today = datetime.now()
        start_date = st.date_input("From Date", value=today)
        end_date = st.date_input("To Date", value=today + timedelta(days=365))
        
        # Refresh button
        st.subheader("🔄 Data Management")
        if st.button("🔄 Refresh Data", type="primary"):
            with st.spinner("Collecting new tournament data..."):
                try:
                    new_tournaments = collect_tournaments()
                    st.success(f"✅ Data refreshed! Collected {len(new_tournaments)} new tournaments")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error refreshing data: {e}")
        
        # Export buttons
        st.subheader("📤 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export CSV"):
                try:
                    export_to_csv()
                    st.success("✅ CSV exported successfully!")
                except Exception as e:
                    st.error(f"❌ Error exporting CSV: {e}")
        
        with col2:
            if st.button("📄 Export JSON"):
                try:
                    export_to_json()
                    st.success("✅ JSON exported successfully!")
                except Exception as e:
                    st.error(f"❌ Error exporting JSON: {e}")
    
    # Main content
    try:
        # Get tournaments based on filters
        sport_filter = None if selected_sport == "All" else selected_sport
        level_filter = None if selected_level == "All" else selected_level
        
        tournaments = get_tournaments_by_filter(sport=sport_filter, level=level_filter)
        
        # Filter by date range
        filtered_tournaments = []
        for tournament in tournaments:
            try:
                start = datetime.strptime(tournament['start_date'], '%Y-%m-%d').date()
                if start_date <= start <= end_date:
                    filtered_tournaments.append(tournament)
            except:
                continue
        
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tournaments", len(filtered_tournaments))
        
        with col2:
            upcoming_count = len([t for t in filtered_tournaments 
                                if datetime.strptime(t['start_date'], '%Y-%m-%d').date() > datetime.now().date()])
            st.metric("Upcoming", upcoming_count)
        
        with col3:
            if filtered_tournaments:
                sports_count = len(set(t['sport'] for t in filtered_tournaments))
                st.metric("Sports", sports_count)
            else:
                st.metric("Sports", 0)
        
        with col4:
            if filtered_tournaments:
                levels_count = len(set(t['level'] for t in filtered_tournaments))
                st.metric("Levels", levels_count)
            else:
                st.metric("Levels", 0)
        
        # AI Insights Section
        st.header("🤖 AI Insights")
        
        if filtered_tournaments:
            # Generate AI insights using Hugging Face
            insights = generate_ai_insights(filtered_tournaments, sport_filter, level_filter)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎯 Recommendations")
                st.write(insights['recommendations'])
            
            with col2:
                st.subheader("📈 Trends")
                st.write(insights['trends'])
        else:
            st.info("No tournaments found for the selected filters. Try adjusting your criteria or refresh the data.")
        
        # Tournament table
        st.header("🏆 Tournament List")
        
        if filtered_tournaments:
            # Convert to DataFrame for better display
            df_data = []
            for tournament in filtered_tournaments:
                df_data.append({
                    'Tournament Name': tournament['tournament_name'],
                    'Sport': tournament['sport'],
                    'Level': tournament['level'],
                    'Start Date': tournament['start_date'],
                    'End Date': tournament['end_date'],
                    'Summary': tournament['summary'][:100] + '...' if len(tournament['summary']) > 100 else tournament['summary']
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Tournament details in expandable sections
            st.subheader("📋 Tournament Details")
            for i, tournament in enumerate(filtered_tournaments[:10]):  # Show first 10
                with st.expander(f"🏆 {tournament['tournament_name']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Sport:** {tournament['sport']}")
                        st.write(f"**Level:** {tournament['level']}")
                        st.write(f"**Start Date:** {tournament['start_date']}")
                        st.write(f"**End Date:** {tournament['end_date']}")
                    
                    with col2:
                        if tournament.get('tournament_url') and tournament['tournament_url'] != 'N/A':
                            st.write(f"**Official URL:** [{tournament['tournament_url']}]({tournament['tournament_url']})")
                        else:
                            st.write("**Official URL:** N/A")
                        
                        st.write(f"**Streaming:** {tournament.get('streaming_links', 'N/A')}")
                        
                        if tournament.get('tournament_image') and tournament['tournament_image'] != 'N/A':
                            try:
                                st.image(tournament['tournament_image'], caption="Tournament Image", width=200)
                            except:
                                st.write("**Image:** Unable to load")
                        else:
                            st.write("**Image:** N/A")
                    
                    st.write(f"**Summary:** {tournament['summary']}")
        else:
            st.warning("No tournaments found matching the current filters.")
        
        # Footer
        st.markdown("---")
        st.markdown("**GenAI Sports Calendar** - Powered by Hugging Face Transformers")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
        logger.error(f"Streamlit app error: {e}")

def generate_ai_insights(tournaments: List[Dict], sport: Optional[str], level: Optional[str]) -> Dict:
    """Generate AI insights using Hugging Face models"""
    try:
        # Initialize Hugging Face models
        collector = TournamentCollector()
        
        if not hasattr(collector, 'models') or not collector.models:
            # Fallback insights without HF models
            return generate_fallback_insights(tournaments, sport, level)
        
        # Generate insights using HF models
        insights = {}
        
        # Generate recommendations
        if tournaments:
            sport_names = [t['sport'] for t in tournaments]
            level_names = [t['level'] for t in tournaments]
            
            # Use HF model to generate recommendations
            prompt = f"Based on {len(tournaments)} tournaments in {sport or 'various sports'} at {level or 'various levels'}, provide 2-3 recommendations for sports fans."
            
            try:
                if 'generator' in collector.models:
                    response = collector.models['generator'](
                        prompt,
                        max_length=150,
                        num_return_sequences=1,
                        do_sample=True,
                        temperature=0.7
                    )
                    insights['recommendations'] = response[0]['generated_text'].replace(prompt, '').strip()
                else:
                    insights['recommendations'] = generate_fallback_insights(tournaments, sport, level)['recommendations']
            except:
                insights['recommendations'] = generate_fallback_insights(tournaments, sport, level)['recommendations']
            
            # Generate trends
            try:
                if 'generator' in collector.models:
                    trend_prompt = f"Analyze trends in {sport or 'sports'} tournaments at {level or 'various levels'} based on {len(tournaments)} events."
                    
                    response = collector.models['generator'](
                        trend_prompt,
                        max_length=120,
                        num_return_sequences=1,
                        do_sample=True,
                        temperature=0.6
                    )
                    insights['trends'] = response[0]['generated_text'].replace(trend_prompt, '').strip()
                else:
                    insights['trends'] = generate_fallback_insights(tournaments, sport, level)['trends']
            except:
                insights['trends'] = generate_fallback_insights(tournaments, sport, level)['trends']
        
        return insights
        
    except Exception as e:
        logger.error(f"Error generating AI insights: {e}")
        return generate_fallback_insights(tournaments, sport, level)

def generate_fallback_insights(tournaments: List[Dict], sport: Optional[str], level: Optional[str]) -> Dict:
    """Generate fallback insights without HF models"""
    insights = {}
    
    if not tournaments:
        insights['recommendations'] = "No tournaments available. Try refreshing the data or adjusting filters."
        insights['trends'] = "Insufficient data for trend analysis."
        return insights
    
    # Simple recommendations based on data
    sport_count = {}
    level_count = {}
    
    for tournament in tournaments:
        sport_count[tournament['sport']] = sport_count.get(tournament['sport'], 0) + 1
        level_count[tournament['level']] = level_count.get(tournament['level'], 0) + 1
    
    top_sport = max(sport_count.items(), key=lambda x: x[1])[0] if sport_count else "various sports"
    top_level = max(level_count.items(), key=lambda x: x[1])[0] if level_count else "various levels"
    
    insights['recommendations'] = f"• Focus on {top_sport} tournaments for the most opportunities\n• {top_level} level events are most common\n• Consider exploring multiple sports for variety"
    
    # Simple trends
    upcoming_count = len([t for t in tournaments 
                         if datetime.strptime(t['start_date'], '%Y-%m-%d').date() > datetime.now().date()])
    
    insights['trends'] = f"• {upcoming_count} upcoming tournaments in the next year\n• {len(sport_count)} different sports represented\n• {len(level_count)} different competition levels available"
    
    return insights

if __name__ == "__main__":
    main()
