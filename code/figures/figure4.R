library(tidyverse)
library(ggpubr)
library(stringr)
library(ggsci)

palette = c("darkorange1", "chartreuse4", "blue3", "magenta")

d.mit <- read.csv("figure4-mit-math-solve-rates.csv", check.names=FALSE)
se <- function(x) sqrt(var(x) / length(x))
d.mit_se <- d.mit %>% pivot_longer(names(d.mit)[2:5], names_to = c("Model"), values_to = c("Accuracy")) %>% group_by(Model) %>% summarize(mean = mean(Accuracy), se = se(Accuracy))
d.mit[1:8,3] <- d.mit[1:8,3] - d.mit[1:8,2]
d.mit[1:8,5] <- d.mit[1:8,5] - d.mit[1:8,4]
d.mit_long <- d.mit %>% pivot_longer(names(d.mit)[2:5], names_to = c("Model"), values_to = c("Accuracy"))
d.mit_long$Course <- factor(d.mit_long$Course, ordered = TRUE)
d.mit_long$Model <- factor(d.mit_long$Model, ordered = TRUE, levels = c("Codex Few-Shot", "Codex Zero-Shot", "GPT-3 CoT", "GPT-3"))

plot.mit <- d.mit_long %>% ggplot(aes(Course, Accuracy, fill = Model)) +
  geom_col(aes(as.numeric(as.factor(Course)) - 0.2, Accuracy, fill = Model), width = 0.4, position = "stack", data = d.mit_long %>% filter(grepl("GPT-3", Model))) +
  geom_col(aes(as.numeric(as.factor(Course)) + 0.2, Accuracy, fill = Model), width = 0.4, position = "stack", data = d.mit_long %>% filter(grepl("Codex", Model))) +
  geom_errorbar(aes(x = 8 - 0.2, y = mean, ymin = mean - se, ymax = mean + se), width = 0.2, position = position_dodge(0.2), data = d.mit_se %>% filter(grepl("GPT-3", Model))) +
  geom_errorbar(aes(x = 8 + 0.2, y = mean, ymin = mean - se, ymax = mean + se), width = 0.2, position = position_dodge(-0.2), data = d.mit_se %>% filter(grepl("Codex", Model))) +
  geom_vline(aes(xintercept = 7.5), linetype = "dotted") +
  scale_fill_manual(values = palette) +
  scale_x_continuous(breaks=1:8, labels=levels(d.mit_long$Course)) +
  scale_y_continuous(limits = c(0, 1)) +
  xlab("MIT Mathematics Courses and a New Columbia Course") +
  ylab("Automatic Solve-Rate") +
  theme_minimal() +
  theme(legend.title = element_blank(), axis.text.x = element_text(angle = 60, hjust = 1))

d.math <- read.csv("figure4-math-solve-rates.csv", check.names=FALSE)
d.math_se <- d.math %>% pivot_longer(names(d.math)[2:5], names_to = c("Model"), values_to = c("Accuracy")) %>% group_by(Model) %>% summarize(mean = mean(Accuracy), se = se(Accuracy))
d.math[1:7,3] <- d.math[1:7,3] - d.math[1:7,2]
d.math[1:7,5] <- d.math[1:7,5] - d.math[1:7,4]
d.math_long <- d.math %>% pivot_longer(names(d.math)[2:5], names_to = c("Model"), values_to = c("Accuracy"))
d.math_long$Topic <- factor(str_wrap(d.math_long$Topic, 10), ordered = TRUE)
d.math_long$Model <- factor(d.math_long$Model, ordered = TRUE, levels = c("Codex Few-Shot", "Codex Zero-Shot", "GPT-3 CoT", "GPT-3"))

plot.math <- d.math_long %>% ggplot(aes(Topic, Accuracy, fill = Model)) +
  geom_col(aes(as.numeric(as.factor(Topic)) - 0.2, Accuracy, fill = Model), width = 0.4, position = "stack", data = d.math_long %>% filter(grepl("GPT-3", Model))) +
  geom_col(aes(as.numeric(as.factor(Topic)) + 0.2, Accuracy, fill = Model), width = 0.4, position = "stack", data = d.math_long %>% filter(grepl("Codex", Model))) +
  geom_errorbar(aes(x = 7 - 0.2, y = mean, ymin = mean - se, ymax = mean + se), width = 0.2, position = position_dodge(0.2), data = d.math_se %>% filter(grepl("GPT-3", Model))) +
  geom_errorbar(aes(x = 7 + 0.2, y = mean, ymin = mean - se, ymax = mean + se), width = 0.2, position = position_dodge(-0.2), data = d.math_se %>% filter(grepl("Codex", Model))) +
  geom_vline(aes(xintercept = 6.5), linetype = "dotted") +
  scale_fill_manual(values = palette) +
  scale_x_continuous(breaks=1:7, labels=levels(d.math_long$Topic)) +
  scale_y_continuous(limits = c(0, 1)) +
  theme_minimal() +
  xlab("MATH Benchmark") +
  ylab("") +
  theme(legend.title = element_blank(), axis.text.y = element_blank(), axis.text.x = element_text(angle = 60, hjust = 1))

ggarrange(plot.mit, plot.math, labels = c("A", "B"), common.legend = TRUE, widths = c(8, 7), align = "hv")

ggsave("figure4-solve-rates.pdf", width = 10, height = 4)

