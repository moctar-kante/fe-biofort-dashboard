
library(readxl)
library(dplyr)
library(ggplot2)
library(purrr)
library(stringr)
library(tibble)
#setwd("~/Project/feBreeding/market_data")
# Define file names and scenario tags
files <- paste0('Scenario ', 1:6, '.xlsx')
scenario_tags <- paste0('Scenario_', 1:6)

# Load and merge
merged_data <- purrr::map2_dfr(files, scenario_tags, ~ {
  df <- read_excel(.x)
  df$scenario <- .y
  df
})
scenario_desc <- tibble(
  scenario = paste0('Scenario_', 1:6),
  assumptions = c(
    '15% adoption, 17% yield, 10% iron',
    '50% adoption, 17% yield, 10% iron',
    '100% adoption, 17% yield, 10% iron',
    '15% adoption, 27.5% yield*, 10% iron',
    '50% adoption, 27.5% yield*, 10% iron',
    '100% adoption, 27.5% yield*, 10% iron'
  )
)
merged_data <- merged_data %>%
  left_join(scenario_desc, by = 'scenario')

region_map <- c(
  # East Africa
  'Burundi' = 'East Africa',
  'Eritrea' = 'East Africa',
  'Ethiopia' = 'East Africa',
  'Kenya' = 'East Africa',
  'Madagascar' = 'East Africa',
  'Rwanda' = 'East Africa',
  'Tanzania' = 'East Africa',
  'Uganda' = 'East Africa',
  
  # West Africa
  'Benin' = 'West Africa',
  'Burkina Faso' = 'West Africa',
  'Ivory Coast' = 'West Africa',
  'Gambia' = 'West Africa',
  'Ghana' = 'West Africa',
  'Guinea' = 'West Africa',
  'Mali' = 'West Africa',
  'Mauritania' = 'West Africa',
  'Niger' = 'West Africa',
  'Nigeria' = 'West Africa',
  'Senegal' = 'West Africa',
  
  # Southern Africa
  'Angola' = 'Southern Africa',
  'Botswana' = 'Southern Africa',
  'Eswatini' = 'Southern Africa',
  'Lesotho' = 'Southern Africa',
  'Malawi' = 'Southern Africa',
  'Mozambique' = 'Southern Africa',
  'Namibia' = 'Southern Africa',
  'South Africa' = 'Southern Africa',
  'Zambia' = 'Southern Africa',
  'Zimbabwe' = 'Southern Africa',
  
  # Central Africa
  'Cameroon' = 'Central Africa',
  'Central African Republic' = 'Central Africa',
  'Democratic Republic of Congo' = 'Central Africa',
  'Republic of Congo' = 'Central Africa',
  'Chad' = 'Central Africa',
  'Comoros' = 'Central Africa',
  
  # North Africa (or part of MENA)
  'Algeria' = 'North Africa',
  'Egypt' = 'North Africa',
  'Libya' = 'North Africa',
  'Morocco' = 'North Africa',
  'Sudan' = 'North Africa',
  'Tunisia' = 'North Africa',
  
  # LAC (Latin America & Caribbean)
  'Argentina' = 'LAC',
  'Belize' = 'LAC',
  'Bolivia' = 'LAC',
  'Brazil' = 'LAC',
  'Chile' = 'LAC',
  'Colombia' = 'LAC',
  'Costa Rica' = 'LAC',
  'Cuba' = 'LAC',
  'Dominica' = 'LAC',
  'Dominican Republic' = 'LAC',
  'Ecuador' = 'LAC',
  'El Salvador' = 'LAC',
  'Guatemala' = 'LAC',
  'Haiti' = 'LAC',
  'Honduras' = 'LAC',
  'Jamaica' = 'LAC',
  'Mexico' = 'LAC',
  'Nicaragua' = 'LAC',
  'Panama' = 'LAC',
  'Paraguay' = 'LAC',
  'Peru' = 'LAC',
  'Uruguay' = 'LAC',
  'Venezuela' = 'LAC',
  'Reunion' = 'LAC',  # Optional
  
  # South Asia
  'Afghanistan' = 'South Asia',
  'Bangladesh' = 'South Asia',
  'Bhutan' = 'South Asia',
  'India' = 'South Asia',
  'Nepal' = 'South Asia',
  'Pakistan' = 'South Asia',
  'Sri Lanka' = 'South Asia',
  'Myanmar' = 'South Asia',
  
  # Southeast Asia
  'Indonesia' = 'Southeast Asia',
  'Laos' = 'Southeast Asia',
  'Philippines' = 'Southeast Asia',
  'Thailand' = 'Southeast Asia',
  'Timor-Leste' = 'Southeast Asia',
  'Vietnam' = 'Southeast Asia',
  
  # MENA (Middle East & North Africa)
  'Bahrain' = 'MENA',
  'Iran' = 'MENA',
  'Iraq' = 'MENA',
  'Israel' = 'MENA',
  'Jordan' = 'MENA',
  'Kuwait' = 'MENA',
  'Lebanon' = 'MENA',
  'Oman' = 'MENA',
  'Palestine' = 'MENA',
  'Qatar' = 'MENA',
  'Saudi Arabia' = 'MENA',
  'Syria' = 'MENA',
  'United Arab Emirates' = 'MENA',
  'Yemen' = 'MENA',
  
  # Central Asia & CIS
  'Armenia' = 'Central Asia',
  'Azerbaijan' = 'Central Asia',
  'Georgia' = 'Central Asia',
  'Kazakhstan' = 'Central Asia',
  'Kyrgyzstan' = 'Central Asia',
  'Tajikistan' = 'Central Asia',
  'Turkmenistan' = 'Central Asia',
  'Uzbekistan' = 'Central Asia',
  
  # Other / Not Classified
  'Turkey' = 'Other',
  'Cyprus' = 'Other'
)

merged_data <- merged_data %>%
  mutate(region = region_map[Country])
merged_data$assumptions <- factor(
  merged_data$assumptions,
  levels = c(
    '15% adoption, 17% yield, 10% iron',
    '15% adoption, 27.5% yield*, 10% iron',
    '50% adoption, 17% yield, 10% iron',
    '50% adoption, 27.5% yield*, 10% iron',
    '100% adoption, 17% yield, 10% iron',
    '100% adoption, 27.5% yield*, 10% iron'
  )
)
#write.csv(merged_data, 'merged_data.csv', row.names = F)
#Relative reduction by scenario
ggplot(merged_data, aes(x = assumptions, y = r_iron_r_2030, fill = region)) +
  geom_boxplot() +
  labs(
    title = 'Relative reduction in iron deficiency',
    x = 'Scenario',
    y = 'Relative reduction (%)'
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

#Absolute reduction in DALYs by scenario
ggplot(merged_data, aes(x = assumptions, y = d_iron_r_2030, fill = region)) +
  geom_boxplot() +
  labs(
    title = 'Absolute reduction in iron deficiency (DALYs)',
    x = 'Scenario',
    y = 'DALYs saved'
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

#Relative reduction by region (across all scenarios)
ggplot(merged_data, aes(x = region, y = r_iron_r_2030, fill = region)) +
  geom_boxplot() +
  labs(
    title = 'Relative reduction by region',
    x = 'Region',
    y = 'Relative reduction (%)'
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1), legend.position = 'none')

#DALYs saved by region (across all scenarios)
ggplot(merged_data, aes(x = region, y = d_iron_r_2030, fill = region)) +
  geom_boxplot() +
  labs(
    title = 'DALYs saved by region',
    x = 'Region',
    y = 'DALYs saved'
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1), legend.position = 'none')

##################
##################

# Filter to priority countries
priority_countries <- c(
  'India', 'Bangladesh', 'Nepal', 'Pakistan', 'Bhutan',
  'Kyrgyzstan', 'Tajikistan', 'Azerbaijan',
  'Peru', 'Bolivia',
  'Bahrain', 'Lebanon'
)

priority_data <- merged_data %>%
  dplyr::filter(Country %in% priority_countries)

# Reorder scenarios
priority_data$assumptions <- factor(
  priority_data$assumptions,
  levels = c(
    '15% adoption, 17% yield, 10% iron',
    '15% adoption, 27.5% yield*, 10% iron',
    '50% adoption, 17% yield, 10% iron',
    '50% adoption, 27.5% yield*, 10% iron',
    '100% adoption, 17% yield, 10% iron',
    '100% adoption, 27.5% yield*, 10% iron'
  )
)

# Plot
ggplot(priority_data, aes(x = assumptions, y = r_iron_r_2030, fill = Country)) +
  geom_col(position = position_dodge2(preserve = "single"), width = 0.7) +
  facet_wrap(~region, scales = 'free_y') +
  labs(
    title = 'Relative reduction in iron deficiency',
    subtitle = 'Priority countries grouped by region',
    x = 'Scenario',
    y = 'Relative reduction (%)'
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 30, hjust = 1),
    legend.position = 'bottom'
  )

# Use the same priority_data subset from earlier

ggplot(priority_data, aes(x = assumptions, y = d_iron_r_2030, fill = Country)) +
  geom_col(position = position_dodge2(preserve = "single"), width = 0.7) +
  facet_wrap(~region, scales = 'free_y') +
  labs(
    title = 'DALYs saved across scenarios',
    subtitle = 'Priority countries grouped by region',
    x = 'Scenario',
    y = 'DALYs saved'
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 30, hjust = 1),
    legend.position = 'bottom'
  )


