library(tidyverse)
library(ggpubr)
library(ggsci)

d <- read.csv("figure5-imports.csv")
d <- subset(d, !grepl("MATH", d$Course.Number))
d.long <- d %>% pivot_longer(cols = names(d)[3:10], names_to = "Library", values_to = "Count")

d.long %>% ggplot(aes(reorder(Course.Number, -Count, sum), Count, fill = Library), alpha = 0.4) +
  geom_col(position = "stack") +
  scale_fill_manual(values = c("#6eb5ff", "#a888d8", "#f28d88", "#c48a88", "#88bebc", "#a8cb88", "#fff5d1", "#f6a6ff", "#88b5e8")) +
  xlab("Course") +
  theme_minimal()

ggsave("figure5-imports.pdf", width = 6, height = 3.2, dpi = 300)

