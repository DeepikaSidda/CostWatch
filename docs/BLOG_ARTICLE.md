# Building a Real-Time AWS Cost Widget: How Kiro Accelerated My Development Journey

**Author:** [Your Name]  
**Published on:** AWS Builder Center  
**Tags:** AWS, Cost Management, Python, Desktop Application, Kiro, AI-Assisted Development

---

## 🎯 The Problem: Console Fatigue

_"I hate checking the bill manager on console, so I built this."_

As a developer working with AWS, I found myself constantly logging into the AWS Console just to check my spending. The workflow was always the same:

1. Open browser → Navigate to AWS Console
2. Sign in (sometimes with MFA)
3. Navigate to Billing Dashboard
4. Wait for the page to load
5. Scroll to find the information I need
6. Close the tab and forget about it until anxiety kicks in again

This 2-minute task, repeated multiple times a day, was eating into my productivity. I needed a solution that would:

- Show my AWS costs **at a glance**
- Stay visible on my desktop **without interrupting my workflow**
- Update **automatically** without manual refresh
- Look **professional** enough to keep on screen during meetings

## 💡 The Solution: AWS Cost Widget

I decided to build a lightweight desktop widget using Python and tkinter that would:

- Display month-to-date AWS spending
- Show a color-coded budget progress bar
- List top spending services
- Auto-refresh at configurable intervals
- Work across Windows, macOS, and Linux

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    AWS Cost Widget                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │   Widget    │  │    Cost     │  │   Scheduler     │ │
│  │     UI      │◄─│   Fetcher   │◄─│   (Auto-refresh)│ │
│  │  (tkinter)  │  │   (boto3)   │  │                 │ │
│  └─────────────┘  └──────┬──────┘  └─────────────────┘ │
│                          │                              │
│                          ▼                              │
│              ┌───────────────────────┐                  │
│              │  AWS Cost Explorer    │                  │
│              │        API            │                  │
│              └───────────────────────┘                  │
└─────────────────────────────────────────────────────────┘
```

## 🚀 How Kiro Accelerated Development

This is where the magic happened. Instead of spending days on boilerplate code, I used **Kiro** - an AI-powered IDE that transformed my development experience.

### 1. Spec-Driven Development

Kiro's spec-driven approach helped me formalize my requirements before writing any code. I started with a rough idea and Kiro helped me create:

**Requirements Document (EARS Format)**

```markdown
### Requirement 1

**User Story:** As a developer, I want to see my month-to-date AWS spending
at a glance, so that I can monitor costs without logging into the AWS Console.

#### Acceptance Criteria

1. WHEN the widget starts THEN the Widget SHALL display the current
   month-to-date cost in a clearly visible format
2. WHEN the month-to-date cost is displayed THEN the Widget SHALL show
   the cost value with currency symbol and two decimal places
```

### 2. Property-Based Testing

Kiro introduced me to property-based testing with Hypothesis. Instead of writing individual test cases, I defined properties that should always hold true:

```python
class TestBudgetColorProperty:
    """
    **Feature: aws-cost-widget, Property 2: Budget color threshold correctness**
    **Validates: Requirements 2.2, 2.3, 2.4**
    """

    @given(st.floats(min_value=0, max_value=74.999, allow_nan=False))
    @settings(max_examples=100)
    def test_green_for_below_75_percent(self, percentage: float):
        """For any percentage below 75, get_budget_color SHALL return green."""
        result = get_budget_color(percentage)
        assert result == COLOR_GREEN
```

This approach caught edge cases I would have never thought to test manually!

### 3. Iterative Design with AI Assistance

When I wanted to enhance the UI, I simply described what I wanted:

> "Make the widget look premium with AWS Cloud Clubs purple theme"

Kiro helped me create a sophisticated color palette:

```python
# Premium Purple Gradient Theme (AWS Cloud Clubs inspired)
COLOR_BG_DEEP = "#0D0221"        # Deep space purple
COLOR_BG_PRIMARY = "#1A0A2E"     # Rich purple black
COLOR_PURPLE_MAIN = "#8B5CF6"    # Primary purple
COLOR_PURPLE_GLOW = "#C4B5FD"    # Soft glow purple
```

### 4. Code Quality & Best Practices

Kiro ensured my code followed best practices:

- **Type hints** for better IDE support
- **Docstrings** for documentation
- **Separation of concerns** (UI, data fetching, configuration)
- **Error handling** for AWS API failures

## 📸 The Final Result

The widget features:

- **Glassmorphism design** with purple gradient borders
- **Real-time cost display** with dynamic color coding
- **Budget progress bar** that changes color based on usage
- **Top 5 services** with ranked indicators
- **Live status indicator** showing auto-refresh is active

### Key Code Snippets

**Cost Fetching with boto3:**

```python
def fetch_aws_costs() -> CostData:
    client = boto3.client('ce')

    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    # Parse and return structured data
    return CostData(
        month_to_date=total_cost,
        top_services=get_top_services(service_costs),
        last_updated=datetime.now()
    )
```

**Premium UI with tkinter:**

```python
# Gradient border effect
outer_glow = tk.Frame(self.root, bg=COLOR_BORDER_OUTER, padx=2, pady=2)
inner_glow = tk.Frame(outer_glow, bg=COLOR_BORDER_GLOW, padx=1, pady=1)

# Large cost display
self.cost_label = tk.Label(
    cost_card, text="$0.00",
    font=("Helvetica", 38, "bold"),
    bg=COLOR_BG_CARD, fg=COLOR_PURPLE_GLOW
)
```

## 📊 Development Metrics

| Metric                 | Without Kiro (Estimated) | With Kiro    |
| ---------------------- | ------------------------ | ------------ |
| Requirements gathering | 2-3 hours                | 30 minutes   |
| Design document        | 3-4 hours                | 45 minutes   |
| Core implementation    | 8-10 hours               | 2 hours      |
| Testing setup          | 2-3 hours                | 30 minutes   |
| UI refinement          | 4-5 hours                | 1 hour       |
| **Total**              | **~20 hours**            | **~5 hours** |

**Kiro reduced my development time by approximately 75%!**

## 🎓 Lessons Learned

1. **Spec-driven development works** - Having clear requirements before coding prevents scope creep
2. **Property-based testing catches edge cases** - 100 random tests > 10 hand-picked tests
3. **AI assistance amplifies productivity** - Focus on _what_ you want, let AI help with _how_
4. **Good design matters** - A premium-looking widget is more likely to stay on your desktop

## 🔗 Resources

- **GitHub Repository:** [aws-cost-widget](https://github.com/yourusername/aws-cost-widget)
- **Kiro IDE:** [kiro.dev](https://kiro.dev)
- **AWS Cost Explorer API:** [Documentation](https://docs.aws.amazon.com/cost-management/latest/APIReference/)

## 🏁 Conclusion

What started as frustration with the AWS Console turned into a polished desktop application. With Kiro's AI-assisted development, I went from idea to production-ready code in a single afternoon.

The widget now sits in the corner of my screen, quietly keeping me informed about my AWS spending. No more console fatigue. No more surprise bills.

**If you hate checking the bill manager on console too, give it a try!**

---

_This article was written as part of the AWS Builder Center community. The project demonstrates how AI-assisted development tools like Kiro can accelerate the creation of practical AWS solutions._

**#AWS #Python #CostManagement #Kiro #AIAssistedDevelopment #AWSCloudClubs**
