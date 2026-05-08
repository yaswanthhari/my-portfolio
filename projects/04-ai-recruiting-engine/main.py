import click
import database
import scraper
import matcher
import generate_resumes
from tabulate import tabulate

@click.group()
def cli():
    """AI Recruiting Engine - Match Candidates to Jobs automatically!"""
    pass

@cli.command()
def init():
    """Initialize the database and generate dummy resumes"""
    click.echo("Initializing system...")
    database.init_db()
    generate_resumes.generate()
    matcher.load_resumes_to_db()
    click.echo("System ready!")

@cli.command()
@click.option('--limit', default=30, help='Number of jobs to scrape')
def scrape(limit):
    """Scrape live jobs from Arbeitnow API"""
    scraper.fetch_jobs(limit=limit)

@cli.command()
def match():
    """Run the NLP matchmaking engine"""
    matcher.match_candidates_to_jobs()

@cli.command()
@click.option('--top', default=10, help='Number of top matches to display')
def report(top):
    """View the best candidate-to-job matches"""
    click.echo(f"\nTop {top} AI Matches:\n")
    results = database.get_top_matches(limit=top)
    
    if not results:
        click.echo("No matches found. Run 'scrape' then 'match' first.")
        return
        
    # Format data for tabulate
    table_data = []
    for row in results:
        # Simplify filename (Yaswanth_Python_Backend.txt -> Yaswanth Python Backend)
        candidate = row['Candidate'].replace('.txt', '').replace('_', ' ')
        score = f"{row['Match_Score']}%"
        # Truncate long job titles
        title = row['Job_Title'][:40] + '...' if len(row['Job_Title']) > 40 else row['Job_Title']
        
        table_data.append([score, candidate, title, row['Company']])
        
    print(tabulate(table_data, headers=["Match", "Candidate", "Job Title", "Company"], tablefmt="grid"))
    
@cli.command()
def run_all():
    """Run the entire pipeline end-to-end"""
    click.echo("Starting Full AI Recruiting Pipeline...\n")
    database.init_db()
    generate_resumes.generate()
    matcher.load_resumes_to_db()
    scraper.fetch_jobs(limit=20)
    matcher.match_candidates_to_jobs()
    
    click.echo("\n==============================================")
    click.echo("              FINAL RESULTS                   ")
    click.echo("==============================================\n")
    
    results = database.get_top_matches(limit=10)
    table_data = []
    for row in results:
        candidate = row['Candidate'].replace('.txt', '').replace('_', ' ')
        score = f"{row['Match_Score']}%"
        title = row['Job_Title'][:40] + '...' if len(row['Job_Title']) > 40 else row['Job_Title']
        table_data.append([score, candidate, title, row['Company']])
        
    print(tabulate(table_data, headers=["Match", "Candidate", "Job Title", "Company"], tablefmt="grid"))

if __name__ == '__main__':
    cli()
