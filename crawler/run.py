import argparse
import asyncio
from crawler.engine import run_from_seed


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", default="crawler/seeds/business_loans.yaml")
    args = p.parse_args()
    asyncio.run(run_from_seed(args.seed))


if __name__ == "__main__":
    main()
