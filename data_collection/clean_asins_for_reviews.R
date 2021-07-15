
###################
## Load Packages ##
###################
if (!require("pacman")) install.packages("pacman")

pacman::p_load(
  tidyverse, 
  haven
)


###############
## Set Paths ##
###############

sinfo <- data.frame(Sys.info())
machine <- sinfo$Sys.info..[4]

machine_path <- 
  ifelse(
    machine %in% c("sussman-rp-mbpro.local", "sussman-rp-mbpro.lan"), 
    "/Users/djolear/Google Drive/", 
    "G:/My Drive/"
  )


file_list <-
  data.frame(
    file_list = list.files(path = paste0(machine_path, "research/projects/emcr/emcr_amzcr_data/amazon_product_info_second_pass"))
  )

file_list <-
  file_list %>% 
  filter(str_detect(file_list, "csv")) %>% 
  mutate(
    product_type = str_extract(file_list, regex(".*(?=_wpi.csv)"))
  )

check_clean_asins <- function(file_name, product_type){
  
  df <-
    read_csv(paste0(machine_path, "research/projects/emcr/emcr_amzcr_data/amazon_product_info_second_pass/", file_name)) 
  
  df <-
    df %>% 
    mutate(
      reviewCount = as.numeric(ifelse(reviewCount == "1 rating", 1, reviewCount))
    )
  
  df_asins_checked_cleaned <-
    df %>% 
    filter(reviewCount > 9) %>% 
    dplyr::select(Name, asin_number)
  
  write_csv(df_asins_checked_cleaned, paste0(machine_path, "research/projects/emcr/emcr_amzcr_data/asins_checked_cleaned/", product_type, "_asins_checked_cleaned.csv"))
  
}

for(i in 1:length(file_list$file_list)) {
  check_clean_asins(file_list$file_list[i], file_list$product_type[i])
}

