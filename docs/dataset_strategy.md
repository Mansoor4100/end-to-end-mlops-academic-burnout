Dataset Strategy
1️⃣ Data Source

This project uses synthetic data to simulate student activity on a learning management system (LMS).

Reasoning:

Real student data is sensitive and restricted

Synthetic data allows controlled experimentation

Enables reproducibility and safe public sharing

2️⃣ Data Granularity

The dataset is modeled at a student × day level.

Definition:

Each row represents one student’s activity on one calendar day

Time-based patterns enable trend and drift analysis

Why this granularity?

Captures gradual behavioral change

Supports rolling-window features (7-day, 14-day)

Enables early burnout detection instead of post-failure analysis

3️⃣ Feature Design Philosophy

Features are derived from behavioral engagement patterns, not academic outcomes.

Examples:

Login frequency

Assignment submission delay trends

Engagement consistency

Late-night and weekend activity patterns

Grades are intentionally excluded to avoid lagging indicators.

4️⃣ Label Strategy (Most Important)

Burnout labels are behavior-based, not self-reported or grade-based.

Label Logic (Conceptual):
A student is labeled as high burnout risk if:

Sustained decline in engagement over multiple days

Increased assignment delays

Increased inactivity streaks

Reduced consistency in study behavior

Labels are generated using rule-based heuristics applied over rolling windows.

Classes:

Low – stable or improving engagement

Medium – mild but consistent decline

High – sustained behavioral deterioration

5️⃣ Prediction Horizon

The model is designed to predict burnout risk 14–21 days ahead, enabling early intervention.

6️⃣ Assumptions

Behavioral changes precede academic failure

Engagement patterns are predictive of burnout

Synthetic patterns approximate real LMS behavior

7️⃣ Limitations

Synthetic data may not capture all real-world nuances

Labels are heuristic-based, not clinically validated

Model predictions are advisory, not diagnostic