library(tidyverse)
library(ggpubr)
library(ggsci)
library(patchwork)
library(lme4)
library(emmeans)
library(Rmisc)
library(qualtRics)

d <- read_survey("figure7-survey.csv")
d <- d %>% subset(StartDate >= as.Date("2021-12-24"))
d <- d %>% subset(Finished)
names(d) <- names(d) %>% sapply(function(x) sub("_", " ", x))
d.long <- d %>% pivot_longer(names(d)[19:198], names_sep = " ", names_to = c("Course", "Source", "Question"), values_to = "Response", values_transform = c(Response = as.character)) %>% subset(!is.na(Question))
d.long <- d.long %>% separate("Question", c("Question", "SubQuestion"), "_")
d <- d.long %>% pivot_wider(id_cols = c("ResponseId", "Course", "Source", "SubQuestion"), names_from = "Question", values_from = "Response")
names(d) <- c(names(d)[1:4], c("Generated", "Appropriate", "Difficulty"))
d$Generated <- factor(d$Generated, ordered = TRUE, levels = c("Human Written", "Machine Generated"))
d$Appropriate <- factor(d$Appropriate, ordered = TRUE, levels = c("Not Appropriate", "Appropriate"))
d$Difficulty <- as.numeric(d$Difficulty)
d$Course <- factor(d$Course, ordered = TRUE, levels = c("18.01", "18.02", "18.03", "18.05", "18.06", "6.042"))
d$Correct <- ((d$Source == "Original") & (d$Generated == "Human Written")) | ((d$Source == "Generated") & (d$Generated == "Machine Generated"))
d$SubQuestion[is.na(d$SubQuestion)] <- 0
d$SubQuestion <- d$SubQuestion %>% as.numeric() %>% sapply(function(x) x + 1) %>% factor(ordered = TRUE, levels = 1:7)
d$Source[d$Source == "Original"] <- "Human Written"
d$Source[d$Source == "Generated"] <- "Machine Generated"
levels(d$Generated) <- c("Rated as Human Written", "Rated as Machine Generated")
levels(d$Appropriate) <- c("Rated as Not Appropriate", "Rated as Appropriate")

plot.diff <- d %>% summarySE("Difficulty", c("Course", "Source")) %>% ggplot(aes(Course, Difficulty, fill = Source, color = Source)) +
  geom_pointrange(aes(ymin = Difficulty - ci, ymax = Difficulty + ci), position = position_dodge(0.4)) +
  scale_fill_d3() +
  scale_color_d3() +
  scale_y_continuous(limits = c(1, 5), breaks = 1:5) +
  annotate("text", x = 0.9, y = 3.4, color = pal_d3()(2)[1], hjust = 0, label = "Machine Generated") +
  annotate("text", x = 1.1, y = 3, color = pal_d3()(2)[2], hjust = 0, label = "Human Written") +
  theme_minimal() +
  theme(legend.position = "none")

plot.app <- d %>% ggplot(aes(Course, fill = Appropriate)) +
  geom_bar(position = "fill", alpha = 0.9) +
  facet_grid( ~ Source) +
  scale_fill_manual(values = c("darkred", "darkgreen")) +
  theme_minimal() +
  ylab("Pct.") +
  theme(axis.text.x = element_text(angle = 0, size = 10), legend.position = "bottom", legend.title = element_blank())

plot.gen <- d %>% ggplot(aes(Course, fill = Generated)) +
  geom_bar(position = "fill", alpha = 0.9) +
  facet_grid( ~ Source) +
  scale_fill_simpsons() +
  theme_minimal() +
  ylab("Pct.") +
  geom_hline(aes(yintercept = 0.5), linetype = "dashed", color = "gray40") +
  theme(axis.text.x = element_text(angle = 0, size = 10), legend.position = "bottom", legend.title = element_blank())

patchwork <- plot.diff / (plot.app + plot.gen)
patchwork + plot_layout(heights = c(2, 1)) + plot_annotation(tag_levels = "A") & theme(plot.tag = element_text(size = 12, face = "bold"))
ggsave("figure7-survey.pdf", width = 12, height = 6)

