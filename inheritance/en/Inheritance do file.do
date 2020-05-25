clear

use "D:\anano\ბლოგები\inheritance blog - CB 2019\Final data\CB2019_Georgia_response_30Jan2020.dta" , clear

set more off


/// weights
 svyset PSU [pweight=INDWT], strata(SUBSTRATUM) fpc(NPSUSS)singleunit(certainty)  || ID, fpc(NHHPSU) || _n, fpc(NADHH)



/// blog 2 - recodes - Who should inherit the apartment: girl or boy

recode APTINHERT (1=1) (2=3) (3=2) (-1=.) (-2=.) (4=.) (-3=.) (-7=.) (-9=.) , gen(aptinhertREC)
label var aptinhertREC "Who should inherit the apartment: girl or boy"

label define aptinhertREC 1 "A daughter", modify
label define aptinhertREC 2 "Should be equally distributed", modify
label define aptinhertREC 3 "A son", modify

label values aptinhertREC aptinhertREC
fre aptinhertREC
fre aptinhertREC

/// blog 2 - recodes - Who should take care of parents more: girl or boy

recode CAREPRNTS (1=2) (2=1) (3=3) (-1=.) (-2=.) (4=.) (-3=.) (-7=.) (-9=.) , gen(careprntsREC)
label var careprntsREC "Who should take care of parents: girl or boy"

label define careprntsREC 1 "A daughter should take care", modify
label define careprntsREC 2 "A son should take care", modify
label define careprntsREC 3 "Should take care equally", modify

label values careprntsREC careprntsREC
svy: tab careprntsREC
fre CAREPRNTS

//1 recode - From what age do you think it is acceptable for a woman to: Drink strong alcohol

recode ACCVODK (-5=1) (16/60=0) (61/100=1) (10/15=-3) (-1=.) (-2=.) (-3=.) (-7=.) (-9=.) , gen(accvodkREC)
label var accvodkREC "Is it acceptable for a woman to: Drink strong alcohol"

label define accvodkREC 1 "Unacceptable", modify
label define accvodkREC 0 "Acceptable from some age", modify
label values accvodkREC accvodkREC
svy: tab accvodkREC


//2 recode - From what age do you think it is acceptable for a woman to: Smoke tobacco

recode ACCTOBA (-5=1) (16/60=0) (61/100=1) (10/15=-3) (-1=.) (-2=.) (-3=.) (-7=.) (-9=.) , gen(acctobaREC)
label var acctobaREC "Is it acceptable for a woman to: Smoke tobacco"

label define acctobaREC 1 "Unacceptable", modify
label define acctobaREC 0 "Acceptable from some age", modify
label values acctobaREC acctobaREC
svy: tab acctobaREC


//3 recode - From what age do you think it is acceptable for a woman to: Live separately from parents before marriage 
recode ACCSEPL (-5=1) (16/60=0) (61/100=1) (10/15=-3) (-1=.) (-2=.) (-3=.) (-7=.) (-9=.) , gen(accseplREC)
label var accseplREC "Is it acceptable for a woman to: Live separately"

label define accseplREC 1 "Unacceptable", modify
label define accseplREC 0 "Acceptable from some age", modify
label values accseplREC accseplREC
svy: tab accseplREC


//4 recode - From what age do you think it is acceptable for a woman to: Have RESPSEXual relations before marriage

recode ACCSEBM (-5=1) (16/60=0) (61/100=1) (10/15=-3) (-1=.) (-2=.) (-3=.) (-7=.) (-9=.) , gen(accsebmREC)
label var accsebmREC "Is it acceptable for a woman to:having RESPSEX before marrige"

label define accsebmREC 1 "Unacceptable", modify
label define accsebmREC 0 "Acceptable from some age", modify
label values accsebmREC accsebmREC
svy: tab accsebmREC


//6 recode - From what age do you think it is acceptable for a woman to: Cohabitate 
recode ACCCOHB (-5=1) (16/60=0) (61/100=1) (10/15=-3) (-1=.) (-2=.) (-3=.) (-7=.) (-9=.) , gen(acccohbREC)
label var acccohbREC "Is it acceptable for a woman to: Cohabitate"

label define acccohbREC 1 "Unacceptable", modify
label define acccohbREC 0 "Acceptable from some age", modify
label values acccohbREC acccohbREC
svy: tab acccohbREC


/// Index of conservative values

foreach var of varlist  accvodkREC acctobaREC accseplREC accsebmREC acccohbREC {
recode `var' (-9/-1=.)
}

gen conservative_index = accvodkREC + acctobaREC + accseplREC + accsebmREC + acccohbREC



/// recodes - sett type

recode SUBSTRATUM (1=1) (6=2) (7=2) (8=2) (9=2) (2=3) (3=3) (4=3) (5=3) (-1=.) (-2=.) (-3=.) (-7=.) (-9=.) , gen(settypeREC)
label var settypeREC "Settlement type"

label define settypeREC 1 "Capital", modify
label define settypeREC 2 "Other Urban", modify
label define settypeREC 3 "Rural", modify
label values settypeREC settypeREC
svy: tab settypeREC


/// Wealth index

foreach var of varlist  OWNCOTV OWNDIGC OWNWASH OWNFRDG OWNAIRC OWNCARS OWNLNDP OWNCELL OWNCOMP {
recode `var' (-9/-1=.)
}

gen wealth_index = OWNCOTV + OWNDIGC + OWNWASH + OWNFRDG + OWNAIRC + OWNCARS + OWNLNDP + OWNCELL + OWNCOMP


/// recodes - Ethnicity type

recode ETHNIC (3=1) (1=2) (2=2) (4=2) (5=2) (6=2) (7=2) (-1=.) (-2=.) (-3=.) (-7=.) (-9=.) , gen(ETHNICREC)
label var ETHNICREC "Ethnicity"

label define ETHNICREC 1 "Ethnic Georgians", modify
label define ETHNICREC 2 "Ethnic Minority", modify

label values ETHNICREC ETHNICREC



/// recodes - education
recode RESPEDU (1=1) (2=1) (3=1) (4=1) (5=2) (6=3) (7=3) (8=3)  (-1=.) (-2=.) (-3=.) (-7=.) (-9=.) , gen(RESPEDUrec)
label var RESPEDUrec "Respondent's education level"

label define RESPEDUrec 1 "Secondary or lower", modify
label define RESPEDUrec 2 "Secondary technical", modify
label define RESPEDUrec 3 "Higher than secondary", modify
label define RESPEDUrec 98 "DKRA", modify
label values RESPEDUrec RESPEDUrec


/// recodes - age groups

recode RESPAGE (18/35=1) (36/55=2) (56/130=3) (-3=.) (-7=.) (-9=.) , gen(AGEGROUP)
label var AGEGROUP "Age group of respondent"

label define AGEGROUP 1 "18-35", modify
label define AGEGROUP 2 "36-55", modify
label define AGEGROUP 3 "Older than 55", modify
label values AGEGROUP AGEGROUP



// regression analysis

/// mlogit - aptinhertREC - Who should inherit the apartment: girl or boy

svy: mlogit aptinhertREC i.RESPSEX i.AGEGROUP b03.settypeREC b01.ETHNICREC b03.RESPEDUrec c.conservative_index , base (1)  
margins, dydx(*) predict(outcome(1)) post
estimates store Daughter

svy: mlogit aptinhertREC i.RESPSEX i.AGEGROUP b03.settypeREC b01.ETHNICREC b03.RESPEDUrec c.conservative_index , base (1)  
margins, dydx(*) predict(outcome(2)) post
estimates store Equally

svy: mlogit aptinhertREC i.RESPSEX i.AGEGROUP b03.settypeREC b01.ETHNICREC b03.RESPEDUrec c.conservative_index , base (1)  
margins, dydx(*) predict(outcome(3)) post
estimates store Son


coefplot Daughter || Equally || Son, drop(_cons) xline(0) byopts(xrescale) 
/// title("Who should inherit the apartment: girl or boy" "By demographic variables and conservative_index", color(dknavy*.9) tstyle(size(medium)) span)
/// subtitle("Marginal effects, 95% CIs", color(navy*.8) tstyle(size(msmall)) span)
/// note("CB 2019/CRRC-Georgia, DEC 2019")


stop


// predicted probabilities 
svy: mlogit aptinhertREC conservative_index
margins, at(conservative_index=(0 1 2 3 4 5))
marginsplot




/*// Ordered Logit Regression - Predicted probabilities - conservative index
svy: ologit aptinhertREC  ETHNICREC settypeREC AGEGROUP RESPSEX RESPEDUrec conservative_index
margins, dydx(*) post
marginsplot, horizontal xline(0) yscale(reverse) recast(scatter)

stop

svy: ologit aptinhertREC conservative_index
margins, at(conservative_index=(0 1 2 3 4 5))
marginsplot


margins, at(conservative_index=(1/5)) predict(outcome(1)) atmeans
margins, at(conservative_index=(1/5)) predict(outcome(2)) atmeans
margins, at(conservative_index=(1/5)) predict(outcome(3)) atmeans
marginsplot

// Ordered Logit Regression - Predicted probabilities - wealth index

svy: ologit aptinhertREC  settypeREC AGEGROUP RESPSEX RESPEDUrec wealth_index
margins, dydx(*) post
marginsplot, horizontal xline(0) yscale(reverse) recast(scatter)

svy: ologit aptinhertREC  settypeREC AGEGROUP RESPSEX RESPEDUrec wealth_index
margins, at(wealth_index=(0 1 2 3 4 5 6 7 8 9))
marginsplot


