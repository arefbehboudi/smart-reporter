import argparse

from src.core.report_generator import run


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Jira-based text report.")
    parser.add_argument(
        "--jql",
        dest="jql",
        help="Optional JQL to override default filters.",
    )
    args = parser.parse_args()

    output_path = run(jql=args.jql)
    print(f"Report generated at: {output_path}")


if __name__ == "__main__":
    main()
