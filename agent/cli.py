"""Usage: python -m agent.cli "Which campaign had the lowest ROAS in September 2026?" """
import sys

from agent.agent import ask


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    r = ask(" ".join(sys.argv[1:]))
    if r.error:
        sys.exit(f"Error: {r.error}")
    print(r.answer)
    if r.value is not None:
        print(f"\nValue: {r.value} {r.unit or ''}")
    if r.sql:
        print(f"\nSQL:\n{r.sql}")
    print(f"\n{len(r.queries)} queries · {r.latency_s}s · ${r.cost_usd:.4f}")


if __name__ == "__main__":
    main()
