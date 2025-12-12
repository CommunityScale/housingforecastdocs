# CommunityScale Housing Market Demand Methodology

## Overview

The Market Demand model forecasts housing demand by price point, tenure (rent vs. own), and bedroom count for households moving within the next year within a region and then scales the demand based on the capture rate for a specific planning area. This methodology combines population projections, household formation forecasts, and detailed microdata on household preferences to generate granular market demand estimates that reflect realistic household behavior and willingness to pay for housing.

## Regional Market Area Definition

The model defines the regional market area as all census PUMAs (Public Use Microdata Areas) within approximately 30 minutes driving time of the local jurisdiction boundary. This geographic definition is based on the principle that housing markets function regionally rather than at municipal boundaries—households search for housing across a commutable area, and developers compete for buyers across this broader region.

**PUMA Selection Process**: The model creates an isochrone polygon representing the 30-minute drive time from the jurisdiction boundary, then identifies all PUMAs with at least 90% of their area within this polygon. This ensures that the regional PUMS data captures the full competitive market area while maintaining geographic precision.

**Rationale for 30-Minute Threshold**: A 30-minute commute represents a widely accepted threshold for reasonable travel-to-work distances and captures the practical geographic extent over which households consider housing options. This definition aligns with housing market research showing that most homebuyers and renters search within a 20-40 minute commute radius of their employment or desired location.

## Methodology Components

### 1. Population and Household Projections

The model begins with demographic projections that establish the baseline for future housing demand:

**Population Forecasting**: The model uses the population projection methodology (described separately) to forecast population by age group and sex. This demographic foundation accounts for aging patterns, birth rates, and historical population trends.

**Household Formation**: Future households are projected by translating population projections into household counts by applying:
- Population proportions by household type
- Population-to-household ratios

These parameters are derived from Public Use Microdata Sample (PUMS) data and capture the relationship between demographic characteristics and household formation patterns.

**Household Type Classification**: The model classifies households into types based on size and presence of children, which are strong predictors of housing demand patterns. Household types include:
- 1-person households (no children)
- 2-person households with and without children
- 3-person households by number of adults and children
- 4-person households by number of adults and children
- 5-person households by number of adults and children
- 6-person households by number of adults and children
- 7+ person households by number of adults and children

This classification enables the model to capture how different household compositions (e.g., single adults, couples without children, families with young children) have distinct preferences for bedroom counts, tenure, and willingness to pay for housing.

### 2. Mover Identification and Forecasting

Not all households participate in the housing market each year. The model focuses on "movers"—households that changed residence within the past year—as these represent active housing demand.

**Mover Share Forecasting**: Historical mover shares by household type are forecast using compositional time series methods, ensuring that shares across household types sum to 1 while accounting for temporal trends.

**Mover Counts**: Projected mover shares are applied to household type projections to estimate the number of moving households by type. These are then aggregated to produce total annual mover counts.

### 3. Income Distribution of Movers

Household income is a primary determinant of housing affordability and demand. The model tracks income distributions for movers to understand what households can afford to pay for housing.

**Income Group by Tenure**: Movers are classified by income group and tenure (owner vs. renter). Historical proportions are forecast compositionally to maintain realistic distributions that sum to 1.

**Income Grouping**: Households are divided into income groups based on Area Median Income (AMI) percentages (e.g., 0-30% AMI, 30-50% AMI, 50-80% AMI, 80-100% AMI, 100-120% AMI, 120%+ AMI). These bins align with housing policy frameworks and enable analysis of affordability across the income spectrum.

**Income-to-Cost Conversion**: To translate household incomes into affordable housing costs, the model converts annual income thresholds to monthly housing cost thresholds. For example, if the income bins range from $0 to $30,000, $30,000 to $50,000, etc., the corresponding monthly housing cost bins represent what households in each income group can afford to spend. These cost bins serve as the framework for estimating demand at different price points.

**Modeling Income Heterogeneity Within Groups**: While households are grouped into income bins for analysis, there is substantial income variation within each bin. A household in the "50-80% AMI" group might have an income near the bottom of that range or near the top, leading to different affordable housing costs. To capture this variation, the model fits a log-normal distribution to each income-tenure group using observed means and variances:

μ<sub>log</sub> = log(μ<sub>income</sub>) - σ²<sub>log</sub> / 2

σ²<sub>log</sub> = log(1 + σ²<sub>income</sub> / μ²<sub>income</sub>)

σ<sub>log</sub> = √σ²<sub>log</sub>

where μ<sub>income</sub> is the mean income and σ²<sub>income</sub> is the income variance for each group. This distributional approach enables Monte Carlo simulation that produces realistic demand estimates across housing cost bins. Rather than assuming all households in an income group have the same income (and thus demand housing at exactly the same price point), the model recognizes that households within a group have varying incomes and thus demand housing across a range of price points. This produces smoother, more realistic demand curves.

### 4. Willingness to Pay (WTP)

Households vary in how much of their income they allocate to housing. The model captures this heterogeneity through Willingness to Pay (WTP) distributions:

**WTP Groups**: For each income-tenure combination, the model calculates the proportion of households in 10 WTP bins (5%, 10%, 15%, ..., 50% of income spent on housing).

**85th Percentile WTP**: For each income-tenure group, the model identifies the 85th percentile WTP—the housing cost share at which 85% of households spend that amount or less. This represents a realistic upper bound on what most households in each segment can afford.

**Willingness-to-Pay Scenarios**: The model produces demand estimates under two distinct scenarios that represent different assumptions about household spending behavior:

**Scenario 1: 30% Expenditure Rule**

This scenario assumes all households spend exactly 30% of their gross income on housing, regardless of income level or tenure type. This represents the federal affordability guideline established by HUD and provides a normative benchmark for what households "should" be able to afford under policy standards. Under this scenario:
- A household earning $60,000 annually can afford $1,500/month in housing costs
- A household earning $120,000 annually can afford $3,000/month in housing costs
- The 30% threshold applies uniformly across all income groups and both renters and owners

This scenario is useful for policy analysis and establishing affordability targets, as it reflects the widely-accepted standard that housing costs should not exceed 30% of gross income.

**Scenario 2: 85th Percentile Willingness-to-Pay**

This scenario recognizes that actual household behavior often deviates from the 30% rule. The model first calculates the 85th percentile WTP for each income-tenure group—the spending level at which 85% of households in that segment spend that amount or less. Then, for each household's observed WTP percentage, the model uses whichever is greater: their actual observed WTP or the 85th percentile for their income-tenure group.

For example, if a household in the 50-80% AMI renter group typically spends 35% of income on housing, but the 85th percentile for that group is 40%, the model uses 40%. If another household typically spends 45%, the model uses 45% (since it's already above the 85th percentile). This approach:
- Ensures no household is assumed to spend less than what most (85%) of similar households can afford
- Captures the reality that many households (particularly lower-income renters) spend more than 30% on housing
- Avoids extreme outliers by using the 85th percentile as a floor rather than capturing the full range up to 100%
- Varies by income and tenure, recognizing that different household types have different housing expenditure patterns

For example, lower-income renters often have 85th percentile WTP of 40-50% of income, while higher-income owners may have 85th percentile WTP of 25-35%. The 85th percentile WTP scenario reflects these observed patterns while maintaining stability in projections.

These two scenarios provide bounds on expected demand: the 30% rule represents normative affordability, while the 85th percentile WTP represents observed market behavior.

### 5. Market Demand Simulation

The core demand estimation uses Monte Carlo simulation to translate income distributions and WTP behavior into housing cost demand. This is where the WTP scenarios directly affect the results:

**Simulation Process**: For each combination of income group, tenure type, and WTP group:

1. Draw M = 20,000 household incomes from the log-normal distribution:

   I<sub>i</sub> ~ LogNormal(μ<sub>log</sub>, σ<sub>log</sub>)

2. Convert each income draw to monthly housing expenditure using the WTP percentage:

   H<sub>i</sub> = (I<sub>i</sub> / 12) × (WTP / 100)

   where WTP is the willingness-to-pay percentage for that cell, which differs by scenario:
   - **30% Expenditure scenario**: WTP = 30 for all households
   - **85th Percentile scenario**: WTP = max(observed WTP, 85th percentile WTP) for each income-tenure-WTP group

3. Classify each simulated household into housing cost bins and calculate proportions:

   p<sub>j</sub> = (1/M) × Σ 𝟙[H<sub>i</sub> ∈ bin<sub>j</sub>]

   where 𝟙 is an indicator function

4. Scale proportions by the projected number of households N in that cell:

   D<sub>j</sub> = p<sub>j</sub> × N

5. Aggregate across all income-tenure-WTP cells to produce total demand by housing cost bin:

   Total Demand<sub>j</sub> = ΣΣΣ D<sub>j,income,tenure,WTP</sub>

The WTP percentage in step 2 is the critical point where the two scenarios diverge, directly determining how much each simulated household can afford to spend on housing.

**Cost-to-Price Conversion**: For homeownership, monthly housing cost bins are converted to home price ranges using current mortgage rates from FRED data. The standard mortgage payment formula is rearranged to solve for home price:

Home Price = Monthly Payment × [((1 + r)<sup>n</sup> - 1) / (r × (1 + r)<sup>n</sup>)]

where:
- r = annual interest rate / 12 (monthly interest rate)
- n = loan term in months (typically 360 for a 30-year mortgage)
- Monthly Payment = the monthly housing cost from the cost bins

The term in brackets is the present value of an annuity factor, converting a stream of monthly payments into the equivalent home price that can be financed.

### 6. Bedroom Demand Estimation

The model estimates demand by bedroom count to reflect household size and composition preferences:

**Bedroom Shares by Household Type**: For each household type, the model forecasts the proportion of movers seeking 0, 1, 2, 3, or 4+ bedrooms using compositional forecasting methods.

**Bedroom Counts**: Bedroom shares are applied to mover counts by household type to produce aggregate bedroom demand.

**Bedroom by Tenure**: Separate bedroom distributions are maintained for renters and owners, as these groups exhibit different space preferences.

### 7. Income-Bedroom-Cost Joint Distribution

The final demand estimates integrate income, bedroom preferences, and housing costs into joint distributions. This requires reconciling three separate projections that may not perfectly align:
1. Demand by housing cost bin (from Monte Carlo simulation)
2. Demand by bedroom count (from household type projections)
3. Historical patterns of which bedroom counts are demanded at which price points

**Historical Joint Distributions**: For each income group, the model tabulates historical counts of movers by bedroom count, weighted by WTP proportions to create a baseline matrix **H** representing the historical relationship between housing costs and bedroom counts. 

**Compositional Forecasting**: Historical income-bedroom joint distributions are converted to shares and forecast using ARIMA(0,1,1) models applied to each cell. This produces forecasted shares that maintain realistic patterns over time.

**Demand Simulation with Historical Patterns**: The forecasted shares are used with the Monte Carlo simulation approach to generate preliminary demand by tenure, housing cost bin, and bedroom count.

**Iterative Proportional Fitting via KL Divergence Minimization**: To ensure the final demand estimates align with both marginal constraints while preserving historical patterns, the model uses Kullback-Leibler (KL) divergence minimization via convex optimization.

Given a historical matrix **H** (size m × n) representing bedroom-by-cost distributions, the model finds a matrix **X** that:
1. Matches row totals **r** (demand by cost bin, from WTP simulation)
2. Matches column totals **c** (demand by bedroom count, from household type projections)
3. Minimizes the KL divergence between **X**/T and **H**/T<sub>H</sub>, preserving historical patterns where possible. IPF could be applied to the marginal distributions to match row and column totals without minimizing divergence from historical patterns, however this approach less accurately reflects housing market dynamics where a unit with more bedrooms generally is more expensive and demand is mostly concentrated along a diagonal of the bedroom count x price table. 

**Mathematical Formulation**:

Minimize:

Σ<sub>i=1</sub><sup>m</sup> Σ<sub>j=1</sub><sup>n</sup> KL(x<sub>i,j</sub> / T || h<sub>i,j</sub> / T<sub>H</sub>)

= Σ<sub>i,j</sub> (x<sub>i,j</sub> / T) × log[(x<sub>i,j</sub> / T) / (h<sub>i,j</sub> / T<sub>H</sub>)]

Subject to:
- Σ<sub>j=1</sub><sup>n</sup> x<sub>i,j</sub> = r<sub>i</sub> for all rows i (cost bins)
- Σ<sub>i=1</sub><sup>m</sup> x<sub>i,j</sub> = c<sub>j</sub> for all columns j (bedroom counts)
- x<sub>i,j</sub> ≥ 0 for all i, j

where:
- T = Σ<sub>i</sub> r<sub>i</sub> = Σ<sub>j</sub> c<sub>j</sub> (total projected movers)
- T<sub>H</sub> = Σ<sub>i</sub> Σ<sub>j</sub> h<sub>i,j</sub> (total historical movers)
- KL divergence measures the information lost when using **H**/T<sub>H</sub> to approximate **X**/T

**Tenure Adjustment**: Row and column totals are adjusted to reflect the forecasted split between renters and owners:
- Renter share: TEN_GRP2 / (TEN_GRP1 + TEN_GRP2)
- Owner share: 1 - renter share

**Margin Reconciliation**: When row and column totals do not match (Σr<sub>i</sub> ≠ Σc<sub>j</sub>), the model distributes the difference proportionally across elements to maintain balance.

This optimization approach ensures that the final demand matrix respects both the cost-based constraints (how much households can afford) and bedroom-based constraints (what size units households need) while maintaining realistic historical patterns of which households demand which types of units.

### 8. Local Market Capture Rates

To translate regional demand into local (sub-regional) demand, the model calculates capture rates:

**Household Share**: The proportion of regional households located in the local area, derived from Census data.

**Mover Shares by Tenure**: Separate capture rates for owner-movers and renter-movers, reflecting different geographic mobility patterns by tenure type.

**Bedroom Shares by Tenure**: The local area's share of regional housing stock for each bedroom-tenure combination, capturing local housing inventory patterns.

These capture rates are applied to regional demand estimates to produce local market demand projections.

## Data Sources

### Primary Data Sources

**Public Use Microdata Sample (PUMS)**: American Community Survey (ACS) 5-year PUMS data (2010-2023) provide household-level detail on:
- Demographics (age, sex, household composition)
- Housing characteristics (tenure, bedrooms, mobility status)
- Income (household income, adjusted for inflation)
- Housing costs (gross rent, monthly ownership costs)
- Willingness to pay (calculated from gross rent percentage of income [GRPIP] and owner costs as percentage of income [OCPIP])

Variables include:
- `HINCP`: Household income
- `ADJINC`: Income adjustment factor for inflation
- `TEN`: Tenure (own vs. rent)
- `BDSP`: Number of bedrooms
- `MV`: Moved within the past year
- `GRNTP`: Gross rent
- `SMOCP`: Selected monthly owner costs
- `GRPIP`: Gross rent as percentage of household income
- `OCPIP`: Owner costs as percentage of household income
- `WGTP`: Household weight
- `PWGTP`: Person weight

**Census Bureau Population Data**: ACS 5-year estimates (Tables B01001, B25042, B07013) for:
- Population by age and sex
- Housing units by bedroom count and tenure
- Mobility by tenure

**HUD Income Limits**: U.S. Department of Housing and Urban Development (HUD) publishes annual Area Median Income (AMI) estimates, used to construct AMI-based income bins.

**FRED Mortgage Rates**: Federal Reserve Economic Data (FRED) API provides monthly 30-year fixed mortgage rates, used to convert housing cost bins to home price ranges.

**PUMA Geography Crosswalks**: Census Bureau allocation factors (AFACT) enable consistent geographic definitions across decennial census boundaries (2000, 2010, 2020 PUMAs).

**Inflation Adjustment**: All income and cost values are adjusted to a common year using the income adjustment (ADJINC) and housing adjustment (ADJHSG) factors provided in PUMS data.

**Survey Weighting**: All estimates incorporate household weights (WGTP) to produce population-representative statistics. Margins of error can be calculated using replicate weights (WGTP1-WGTP80) via successive difference replication.

## Key Assumptions

1. **Willingness-to-Pay Scenarios**: The model produces two distinct scenarios. The 30% expenditure rule scenario assumes all households spend exactly 30% of gross income on housing, reflecting federal housing policy guidelines. The 85th percentile WTP scenario incorporates observed market behavior where households in different income-tenure groups spend varying percentages of income on housing.

2. **Log-Normal Income Distribution**: Within each income bin, household incomes are assumed to follow a log-normal distribution, a standard assumption in income modeling that captures right-skewness and provides a realistic representation of income heterogeneity.

3. **Stable Preferences**: Household preferences for bedroom counts and WTP behavior are assumed to change gradually according to observed historical trends, forecasted using compositional time series methods.

4. **Regional Market Behavior**: Households within a 30-minute drive time search for housing across the entire regional market area, competing for available units regardless of municipal boundaries.

5. **Fixed-Rate Mortgages**: Home price affordability calculations assume standard fixed-rate mortgages with constant monthly payments over the loan term, using current market interest rates from FRED data.

6. **Compositional Stationarity**: Time series forecasting of compositional data (shares) assumes that historical trends in relative proportions continue into the future. When forecasting variables that must sum to 1 (e.g., shares across income groups), the model uses the centered log-ratio (CLR) transformation:

   CLR(x) = [log(x₁/g(x)), log(x₂/g(x)), ..., log(x<sub>p</sub>/g(x))]

   where g(x) = (x₁ × x₂ × ... × x<sub>p</sub>)<sup>1/p</sup> is the geometric mean of x.

   This transformation maps compositional data from the simplex (where Σx<sub>i</sub> = 1) to Euclidean space (ℝ<sup>p-1</sup>), where standard time series methods (ARIMA) can be applied. After forecasting in the transformed space, the inverse CLR transformation returns values to the original compositional space:

   x<sub>i</sub> = exp(CLR<sub>i</sub>) / Σ exp(CLR<sub>j</sub>)

   This ensures that forecasted values remain positive and sum to 1.
