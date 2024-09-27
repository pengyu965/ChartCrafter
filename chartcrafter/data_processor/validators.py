supported_chart_types = (
    "line", "grouped vertical bar", "stacked vertical bar", "stacked horizontal bar", "grouped horizontal bar")


def pmc_json_validator(func):
    def verifier(pmc_json):
        error_message = ""
        if (chart_type := (
                pmc_json["task1"].get("output", {}).get("chart_type", "") or "").lower()) not in supported_chart_types:
            error_message = (f"The PMC JSON is missing chart_type attribute"
                             f" or chart_type:{chart_type} is not among {supported_chart_types}")
        elif "task6" not in pmc_json or pmc_json["task6"] is None:
            error_message = "The PMC JSON is missing task6 or the task6 value is None"
        elif not pmc_json:
            error_message = "The PMC JSON is empty or None"

        if error_message:
            raise ValueError(error_message)

        return func(pmc_json)

    return verifier
