import schedule
import time
from automate import auto  

def job():
    print("Placing bets...")
    auto()

def main():
    # Schedule the job every 10 minutes
    schedule.every(10).minutes.do(job)
    
    # You can also schedule at specific times; for example:
    # schedule.every().day.at("12:00").do(job)
    
    print("Scheduler started. Press Ctrl+C to exit.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Scheduler stopped.")

if __name__ == '__main__':
    main()
