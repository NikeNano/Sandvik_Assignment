library(tuneR);
library(seewave);
library(progress);

#setwd("/Users/Niklas/Documents/test")
setwd("/home/niklas_sven_hansson/test")
# function used for feature extraction
# should break this up later on 
feature_extraction <- function(file_path,sample_rate=16000) {
  file_path<-as.character(file_path)
  r <- tuneR::readWave(file_path, from=0, units = "seconds");
  #frequency spectrum analysis
  songspec <- seewave::spec(r, f = sample_rate, plot = FALSE);
  # film is in KHz And Sample rate is in Hz
  analysis <- seewave::specprop(spec=songspec,str=FALSE ,f = sample_rate, flim = c(0, 280/1000), plot = FALSE);
  
  #Store Parameters
  meanfreq <- analysis$mean/1000;
  sd <- analysis$sd/1000;
  median <- analysis$median/1000;
  Q25 <- analysis$Q25/1000;
  Q75 <- analysis$Q75/1000;
  IQR <- analysis$IQR/1000;
  skew <- analysis$skewness;
  kurt <- analysis$kurtosis;
  sp.ent <- analysis$sh;
  sfm <- analysis$sfm;
  mode <- analysis$mode/1000;
  centroid <- analysis$cent/1000;
  
  # Check this out 
  #peakf <- seewave::fpeaks(songspec, f = sample_rate, wl = 512, nmax = 3, plot = FALSE)[1, 1]
  peakf<-0
  #Fundamental frequency parameters
  ff <- seewave::fund(r, f = sample_rate, ovlp = 50, threshold = 5, 
                      fmax = 280, ylim=c(0, 280/1000), plot = FALSE, wl = 512)[, 2];
  meanfun<-mean(ff, na.rm = T);
  minfun<-min(ff, na.rm = T);
  maxfun<-max(ff, na.rm = T);
  
  #Dominant frecuency parameters
  y <- seewave::dfreq(r, f = sample_rate, wl = 512, ylim=c(0, 280/1000), ovlp = 0, plot = F, threshold = 5, bandpass = c(0,7000), fftw = TRUE)[, 2];
  meandom <- mean(y, na.rm = TRUE);
  mindom <- min(y, na.rm = TRUE);
  maxdom <- max(y, na.rm = TRUE);
  dfrange <- (maxdom - mindom);
  duration <- seewave::duration(wave = r, f = sample_rate);
  # Store it to a dataframe/csv later on. 
  ret <- (c(duration, meanfreq, sd, median, Q25, Q75, IQR, skew, kurt, sp.ent, sfm, mode, centroid, peakf, meanfun, minfun, maxfun, meandom, mindom, maxdom, dfrange));
}
preprocess_all_files <- function(path_csv=NA) {
  df <- read.csv(path_csv,head=TRUE)
  df_out<-data.frame(col1=character(0), col2=character(0),col3=character(0), col4=character(0),col5=character(0),col6=numeric(),col7=numeric(),col8=numeric(),col9=numeric(),col10=numeric(),col11=numeric(),col12=numeric(),col13=numeric(),col14=numeric(),col15=numeric(),col16=numeric(),col17=numeric(),col118=numeric(),col19=numeric(),col20=numeric(),col21=numeric(),col22=numeric(),col23=numeric(),col24=numeric(),col25=numeric(),col26=numeric())
  
  pb <- progress_bar$new(total = nrow(df))
  pb$tick(0)
   
  for (i in 1:(nrow(df))) {
    pb$tick() 
    # input for the feature extraction
    path <-df$path[i]
    label <-df$gender[i]
    language <-df$language[i]
    age_range <-df$age_range[i]
    dialect <-df$dialect[i]
    
    features <- feature_extraction(file_path = df$path[i],sample_rate = 16000)
    add<-data.frame(col1=path,col2=label,col3=language,col4=age_range,col5=dialect,col6=features[1],col7=features[2],col8=features[3],col9=features[4],col10=features[5],col11=features[6],col12=features[7],col13=features[8],col14=features[9],col15=features[10],col16=features[11],col17=features[12],col18=features[13],col19=features[14],col20=features[15],col21=features[16],col22=features[17],col23=features[18],col24=features[19],col25=features[20],col26=features[21])
    df_out <- rbind(df_out,add)
  }
  colnames(df_out) <- c("file", "label","language","age_range","dialect","duration", "meanfreq", "sd", "median", "Q25", "Q75", "IQR", "skew", "kurt", "sp.ent", "sfm", "mode", "centroid", "peakf", "meanfun", "minfun", "maxfun", "meandom", "mindom", "maxdom", "dfrange")
  write.csv(df_out,file="ouput2.csv")
}

csv_path = "data.csv"
#file<-"/Users/Niklas/Downloads/pygender/train_data/youtube/male/male1.wav"
preprocess_all_files(csv_path)


#print("Done with the preprocessing")
#file <- "/Users/Niklas/Downloads/Aaron-20080318-kdl/wav/b0019.wav"
#output<-feature_extraction(file_path = file,sample_rate = 16000)


