from dotenv import load_dotenv

# Load env vars
load_dotenv()

from deep_research.mas.graph import mas_app  # noqa: E402


def verify_solution():
    """Runs the solved MAS against the GAIA question."""

    print("\n=== VERIFYING SOLUTION (solutions/mas) ===\n")

    question = """
    Which of the fruits shown in the 2008 painting "Embroidery from Uzbekistan" were served as part of the October 1949 breakfast menu for the ocean liner that was later used as a floating prop for the film "The Last Voyage"? 
    Give the items as a comma-separated list, ordering them in clockwise order based on their arrangement in the painting starting from the 12 o'clock position. Use the plural form of each fruit.
    """

    initial_state = {
        "topic": question,
        "sub_topics": [],
        "research_outputs": [],
        "final_report": "",
    }

    try:
        print("Running MAS from solutions...")
        result = mas_app.invoke(initial_state)
        report = result.get("final_report", "")

        print("\n=== GENERATED REPORT ===\n")
        print(report)
        print("\n========================\n")

        if report and len(report) > 100:
            print("SUCCESS: Report generated.")
        else:
            print("FAILURE: Report too short or empty.")

    except Exception as e:
        print(f"FAILURE: Exception occurred: {e}")


if __name__ == "__main__":
    verify_solution()
