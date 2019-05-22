library(lme4)
library(sjPlot)
library(car)
library(emmeans)
library(parallel)

df <- read.csv('data/all_values.csv', sep=';')
df_ec <- df[df$condition == 'EC', ]

df_wsmi_theta = df_ec[df_ec$marker == 'wsmi_theta', ]
df_wsmi_alpha = df_ec[df_ec$marker == 'wsmi_alpha', ]
df_wpli_theta = df_ec[df_ec$marker == 'wpli_theta', ]
df_wpli_alpha = df_ec[df_ec$marker == 'wpli_alpha', ]
df_plv_theta = df_ec[df_ec$marker == 'plv_theta', ]
df_plv_alpha = df_ec[df_ec$marker == 'plv_alpha', ]

model_wsmi_theta <- lmer(value ~ regions + groupe + regions:groupe + age_M0 + sexe + NSC_bin + apoe4 + (1| ID), data = df_wsmi_theta)
model_wsmi_alpha<- lmer(value ~ regions + groupe + regions:groupe + age_M0 + sexe + NSC_bin + apoe4 + (1| ID), data = df_wsmi_alpha)
model_wpli_theta <- lmer(value ~ regions + groupe + regions:groupe + age_M0 + sexe + NSC_bin + apoe4 + (1| ID), data = df_wpli_theta)
model_wpli_alpha <- lmer(value ~ regions + groupe + regions:groupe + age_M0 + sexe + NSC_bin + apoe4 + (1| ID), data = df_wpli_alpha)
model_plv_theta <- lmer(value ~ regions + groupe + regions:groupe + age_M0 + sexe + NSC_bin + apoe4 + (1| ID), data = df_plv_theta)
model_plv_alpha <- lmer(value ~ regions + groupe + regions:groupe + age_M0 + sexe + NSC_bin + apoe4 + (1| ID), data = df_plv_alpha)
# Anova(model_wsmi_theta, type=2)
print(Anova(model_wsmi_theta, type=2))
print(Anova(model_wsmi_alpha, type=2))
print(Anova(model_wpli_theta, type=2))
print(Anova(model_wpli_alpha, type=2))
print(Anova(model_plv_theta, type=2))
print(Anova(model_plv_alpha, type=2))


# No correction
emm_options(pbkrtest.limit = 10395)
post_hoc_wsmi_theta <- emmeans(model_wsmi_theta, ~regions:groupe, adjust = 'none')
unique_groupe <- c('A-/N-', 'A+/N+', 'A-/N+', 'A+/N-')
tdf <- data.frame(post_hoc_wsmi_theta)

method <- lapply(do.call('cbind', mclapply(unique(tdf$regions), function(c){
  do.call('cbind', lapply(unique_groupe[-length(unique_groupe)], function(g1){
    do.call('cbind', lapply(unique_groupe[(match(g1, unique_groupe)+1):length(unique_groupe)], function(g2){
        contrast <- rep(0, nrow(tdf))
        contrast[which(tdf$regions == c & tdf$groupe == g1)] <- 1
        contrast[which(tdf$regions == c & tdf$groupe == g2)] <- -1
      return(setNames(data.frame(x = contrast), paste(c, '.', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g1))), '_', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g2))), sep = '')))
    }))
  }))
}, mc.cores = 3)), function(x) x)

c_wsmi_theta <- contrast(post_hoc_wsmi_theta, method, adjust = 'none')

c_wsmi_theta_df <- data.frame(c_wsmi_theta)
write.table(c_wsmi_theta_df, 'stats/contrast_wsmi_theta.csv', sep=';')

post_hoc_wsmi_alpha <- emmeans(model_wsmi_alpha, ~regions:groupe, adjust = 'none')
unique_groupe <- c('A-/N-', 'A+/N+', 'A-/N+', 'A+/N-')
tdf <- data.frame(post_hoc_wsmi_alpha)

method <- lapply(do.call('cbind', mclapply(unique(tdf$regions), function(c){
  do.call('cbind', lapply(unique_groupe[-length(unique_groupe)], function(g1){
    do.call('cbind', lapply(unique_groupe[(match(g1, unique_groupe)+1):length(unique_groupe)], function(g2){
        contrast <- rep(0, nrow(tdf))
        contrast[which(tdf$regions == c & tdf$groupe == g1)] <- 1
        contrast[which(tdf$regions == c & tdf$groupe == g2)] <- -1
      return(setNames(data.frame(x = contrast), paste(c, '.', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g1))), '_', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g2))), sep = '')))
    }))
  }))
}, mc.cores = 3)), function(x) x)

c_wsmi_alpha <- contrast(post_hoc_wsmi_alpha, method, adjust = 'none')

c_wsmi_alpha_df <- data.frame(c_wsmi_alpha)
write.table(c_wsmi_alpha_df, 'stats/contrast_wsmi_alpha.csv', sep=';')

# Now for plv_theta

post_hoc_plv_theta <- emmeans(model_plv_theta, ~regions:groupe, adjust = 'none')
unique_groupe <- c('A-/N-', 'A+/N+', 'A-/N+', 'A+/N-')
tdf <- data.frame(post_hoc_plv_theta)

method <- lapply(do.call('cbind', mclapply(unique(tdf$regions), function(c){
  do.call('cbind', lapply(unique_groupe[-length(unique_groupe)], function(g1){
    do.call('cbind', lapply(unique_groupe[(match(g1, unique_groupe)+1):length(unique_groupe)], function(g2){
        contrast <- rep(0, nrow(tdf))
        contrast[which(tdf$regions == c & tdf$groupe == g1)] <- 1
        contrast[which(tdf$regions == c & tdf$groupe == g2)] <- -1
      return(setNames(data.frame(x = contrast), paste(c, '.', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g1))), '_', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g2))), sep = '')))
    }))
  }))
}, mc.cores = 3)), function(x) x)

c_plv_theta <- contrast(post_hoc_plv_theta, method, adjust = 'none')

c_plv_theta_df <- data.frame(c_plv_theta)
write.table(c_plv_theta_df, 'stats/contrast_plv_theta.csv', sep=';')



post_hoc_plv_alpha <- emmeans(model_plv_alpha, ~regions:groupe, adjust = 'none')
unique_groupe <- c('A-/N-', 'A+/N+', 'A-/N+', 'A+/N-')
tdf <- data.frame(post_hoc_plv_alpha)

method <- lapply(do.call('cbind', mclapply(unique(tdf$regions), function(c){
  do.call('cbind', lapply(unique_groupe[-length(unique_groupe)], function(g1){
    do.call('cbind', lapply(unique_groupe[(match(g1, unique_groupe)+1):length(unique_groupe)], function(g2){
        contrast <- rep(0, nrow(tdf))
        contrast[which(tdf$regions == c & tdf$groupe == g1)] <- 1
        contrast[which(tdf$regions == c & tdf$groupe == g2)] <- -1
      return(setNames(data.frame(x = contrast), paste(c, '.', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g1))), '_', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g2))), sep = '')))
    }))
  }))
}, mc.cores = 3)), function(x) x)

c_plv_alpha <- contrast(post_hoc_plv_alpha, method, adjust = 'none')

c_plv_alpha_df <- data.frame(c_plv_alpha)
write.table(c_plv_alpha_df, 'stats/contrast_plv_alpha.csv', sep=';')


# FDR Correction

emm_options(pbkrtest.limit = 10395)
post_hoc_wsmi_theta <- emmeans(model_wsmi_theta, ~regions:groupe, adjust = 'none')
unique_groupe <- c('A-/N-', 'A+/N+', 'A-/N+', 'A+/N-')
tdf <- data.frame(post_hoc_wsmi_theta)

method <- lapply(do.call('cbind', mclapply(unique(tdf$regions), function(c){
  do.call('cbind', lapply(unique_groupe[-length(unique_groupe)], function(g1){
    do.call('cbind', lapply(unique_groupe[(match(g1, unique_groupe)+1):length(unique_groupe)], function(g2){
        contrast <- rep(0, nrow(tdf))
        contrast[which(tdf$regions == c & tdf$groupe == g1)] <- 1
        contrast[which(tdf$regions == c & tdf$groupe == g2)] <- -1
      return(setNames(data.frame(x = contrast), paste(c, '.', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g1))), '_', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g2))), sep = '')))
    }))
  }))
}, mc.cores = 3)), function(x) x)

c_wsmi_theta <- contrast(post_hoc_wsmi_theta, method, adjust = 'fdr')

c_wsmi_theta_df <- data.frame(c_wsmi_theta)
write.table(c_wsmi_theta_df, 'stats/contrast_wsmi_theta_fdr.csv', sep=';')

post_hoc_wsmi_alpha <- emmeans(model_wsmi_alpha, ~regions:groupe, adjust = 'none')
unique_groupe <- c('A-/N-', 'A+/N+', 'A-/N+', 'A+/N-')
tdf <- data.frame(post_hoc_wsmi_alpha)

method <- lapply(do.call('cbind', mclapply(unique(tdf$regions), function(c){
  do.call('cbind', lapply(unique_groupe[-length(unique_groupe)], function(g1){
    do.call('cbind', lapply(unique_groupe[(match(g1, unique_groupe)+1):length(unique_groupe)], function(g2){
        contrast <- rep(0, nrow(tdf))
        contrast[which(tdf$regions == c & tdf$groupe == g1)] <- 1
        contrast[which(tdf$regions == c & tdf$groupe == g2)] <- -1
      return(setNames(data.frame(x = contrast), paste(c, '.', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g1))), '_', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g2))), sep = '')))
    }))
  }))
}, mc.cores = 3)), function(x) x)

c_wsmi_alpha <- contrast(post_hoc_wsmi_alpha, method, adjust = 'fdr')

c_wsmi_alpha_df <- data.frame(c_wsmi_alpha)
write.table(c_wsmi_alpha_df, 'stats/contrast_wsmi_alpha_fdr.csv', sep=';')

# Now for plv_theta

post_hoc_plv_theta <- emmeans(model_plv_theta, ~regions:groupe, adjust = 'none')
unique_groupe <- c('A-/N-', 'A+/N+', 'A-/N+', 'A+/N-')
tdf <- data.frame(post_hoc_plv_theta)

method <- lapply(do.call('cbind', mclapply(unique(tdf$regions), function(c){
  do.call('cbind', lapply(unique_groupe[-length(unique_groupe)], function(g1){
    do.call('cbind', lapply(unique_groupe[(match(g1, unique_groupe)+1):length(unique_groupe)], function(g2){
        contrast <- rep(0, nrow(tdf))
        contrast[which(tdf$regions == c & tdf$groupe == g1)] <- 1
        contrast[which(tdf$regions == c & tdf$groupe == g2)] <- -1
      return(setNames(data.frame(x = contrast), paste(c, '.', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g1))), '_', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g2))), sep = '')))
    }))
  }))
}, mc.cores = 3)), function(x) x)

c_plv_theta <- contrast(post_hoc_plv_theta, method, adjust = 'fdr')

c_plv_theta_df <- data.frame(c_plv_theta)
write.table(c_plv_theta_df, 'stats/contrast_plv_theta_fdr.csv', sep=';')



post_hoc_plv_alpha <- emmeans(model_plv_alpha, ~regions:groupe, adjust = 'none')
unique_groupe <- c('A-/N-', 'A+/N+', 'A-/N+', 'A+/N-')
tdf <- data.frame(post_hoc_plv_alpha)

method <- lapply(do.call('cbind', mclapply(unique(tdf$regions), function(c){
  do.call('cbind', lapply(unique_groupe[-length(unique_groupe)], function(g1){
    do.call('cbind', lapply(unique_groupe[(match(g1, unique_groupe)+1):length(unique_groupe)], function(g2){
        contrast <- rep(0, nrow(tdf))
        contrast[which(tdf$regions == c & tdf$groupe == g1)] <- 1
        contrast[which(tdf$regions == c & tdf$groupe == g2)] <- -1
      return(setNames(data.frame(x = contrast), paste(c, '.', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g1))), '_', gsub('\\+', 'plus', gsub('-', 'moins', gsub('\\/', '', g2))), sep = '')))
    }))
  }))
}, mc.cores = 3)), function(x) x)

c_plv_alpha <- contrast(post_hoc_plv_alpha, method, adjust = 'fdr')

c_plv_alpha_df <- data.frame(c_plv_alpha)
write.table(c_plv_alpha_df, 'stats/contrast_plv_alpha_fdr.csv', sep=';')
# s <- summary(post_hoc_wsmi_theta)
# ph_wsmi_theta <- as.data.frame(s$contrasts)
# write.csv(ph_wsmi_theta, 'stats/contrast_wsmi_theta.csv')

# post_hoc_plv_theta <- emmeans(model_plv_theta, pairwise~regions:groupe, adjust = 'none')
# s <- summary(post_hoc_plv_theta)
# ph_plv_theta <- as.data.frame(s$contrasts)
# write.csv(ph_plv_theta, 'stats/contrast_plv_theta.csv')


