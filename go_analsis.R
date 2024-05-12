library(ggplot2)
library(clusterProfiler)
library(AnnotationDbi)
library(org.At.tair.db)
library(DOSE)
library(reshape2) 
library(tidyverse)
library(dplyr)
library(ggplot2)
library(RColorBrewer)
library(forcats)
library("xlsx")


fig_go_analsis <- function(HGT_category, title){
  
  HGT_file <- read.delim("HGT_only_YES.txt",header = 1,row.names = 1, sep = "\t")
  
  HGT_file_filter <- HGT_file %>% filter(HGT == HGT_category)
  
  genes_list <- rownames(HGT_file_filter)
  
  
  GO_results <- enrichGO(gene = genes_list, OrgDb = "org.At.tair.db", keyType = "TAIR", ont = "BP")
  GO_results <- as.data.frame(GO_results)
  
  
  GO_results <- mutate(GO_results, fold_enrichment = parse_ratio(GeneRatio) / parse_ratio(BgRatio))
  
  GO_results <- GO_results %>% select(Description, Count ,qvalue, fold_enrichment) %>% 
    arrange(desc(Count)) %>% filter(qvalue <= 0.05)  %>% filter(Count>=2)
  
  GO_results <- GO_results[1:25,] %>% arrange(desc(Description))
  
  GO_results$FDR<-format(GO_results$qvalue, digits = 3)
  
  GO_results$HGT_title <- title
  
  GO_results
  
}

B_P <- fig_go_analsis("B>P", "a. HGT from bacteria to plants")
P_B <- fig_go_analsis("P>B", "b. HGT from plants to bacteria")
B_O <- fig_go_analsis("B>O", "c. HGT from bacteria to eukaryotes")
O_B <- fig_go_analsis("O>B", "d. HGT from eukaryotes to bacteria")




total <- rbind(B_P, P_B, B_O, O_B) 

total <- na.omit(total)

total$fold_enrichment_cat <- cut(total$fold_enrichment,
                                 breaks=c(-1, 1, 5, 10, 50, 100, 500),
                                 labels=c('0-1','1-5', '5-10', '10-50', '50-100', '>100'))

cols <- c(">100" = "#0B0D1E","50-100"= "#184E77", "10-50" = "#1A759F",
          "5-10" = "#34A0A4", "1-5" = "#6DC495", "0-1"="#fafcfb" )

total <- total %>%
  mutate(across(HGT_title, factor, levels=c("a. HGT from bacteria to plants" , "b. HGT from plants to bacteria", "c. HGT from bacteria to eukaryotes", "d. HGT from eukaryotes to bacteria")))



p_1<-ggplot(data=total, aes(x=fct_inorder(Description), y=Count, fill=(fold_enrichment_cat))) +
  geom_bar(stat="identity", position = 'dodge') +
  geom_text(aes(label=FDR), hjust=1.1, color="white", size=8, fontface='bold') +
  coord_flip() +
  scale_fill_manual(values = cols, name = "Fold\nEnrichment")+
  scale_y_continuous(breaks=c(0,2,4,6,8,10)) +
  xlab("") + 
  ylab("Genes involved in the term")+
  facet_wrap(~HGT_title, scales = "free", nrow = 4)+
  theme_bw(base_size = 35) +
  theme(legend.key.size = unit(1, 'cm'), strip.background =element_blank(),
        strip.text.x = element_text(size=42))




p_1
ggsave("Figure_2.clusterProfiler.png",plot = p_1, width = 30,height = 40)
ggsave("Figure_2.clusterProfiler.JPEG",plot = p_1, width = 30,height = 40)


