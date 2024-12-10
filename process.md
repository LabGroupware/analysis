|    | LastActionCode                                        |   TotalTime_count |   TotalTime_mean |   TotalTime_max |   TotalTime_min |   TotalTime_median |    TotalTime_var |   thread | action              |   record_count |
|---:|:------------------------------------------------------|------------------:|-----------------:|----------------:|----------------:|-------------------:|-----------------:|---------:|:--------------------|---------------:|
|  0 | CREATE_USER_PREFERENCE                                |               485 |        17965     |           25860 |            7913 |            19396   |      2.12063e+07 |      500 | create_user_profile |           1458 |
|  1 | CREATE_USER_PROFILE                                   |               487 |        11708.1   |           17693 |            3873 |            11722   |      8.03733e+06 |      500 | create_user_profile |           1458 |
|  2 | CREATE_FILE_OBJECT                                    |               493 |        19654.2   |           27377 |            5172 |            19466   |      9.97058e+06 |      500 | create_file_object  |           1482 |
|  3 | VALIDATE_FILE_OBJECT                                  |               495 |         5537.11  |           12282 |             767 |             5793   |      7.44349e+06 |      500 | create_file_object  |           1482 |
|  4 | CREATE_DEFAULT_TEAM_AND_ADD_INITIAL_DEFAULT_TEAM_USER |               266 |        29861.3   |           34730 |           22291 |            30629.5 |      8.80986e+06 |      500 | create_organization |           1330 |
|  5 | CREATE_ORGANIZATION_AND_ADD_INITIAL_ORGANIZATION_USER |               266 |        21856.6   |           25944 |           15772 |            22493   |      6.00169e+06 |      500 | create_organization |           1330 |
|  6 | VALIDATE_ORGANIZATION                                 |               266 |         3720.05  |            6863 |             986 |             3381   |      1.80343e+06 |      500 | create_organization |           1330 |
|  7 | VALIDATE_USER                                         |               266 |        15122.1   |           17267 |           10408 |            14984   | 798399           |      500 | create_organization |           1330 |
|  8 | CREATE_TEAM_AND_ADD_INITIAL_TEAM_USER                 |                89 |        18129.3   |           19668 |           15806 |            18127   | 871850           |      500 | create_team         |            368 |
|  9 | VALIDATE_ORGANIZATION_AND_ORGANIZATION_USER_EXIST     |                95 |        15042     |           18618 |           11237 |            15050   | 917743           |      500 | create_team         |            368 |
| 10 | VALIDATE_TEAM                                         |                95 |         2260.55  |            7073 |             737 |             2395   |      1.15539e+06 |      500 | create_team         |            368 |
| 11 | CREATE_TASK_AND_ATTACH_FILE_OBJECT                    |               406 |        39371.2   |           44893 |           28544 |            40020.5 |      1.61217e+07 |      500 | create_task         |           2442 |
| 12 | VALIDATE_FILE_OBJECT                                  |               408 |        30173.9   |           35595 |           20310 |            31032   |      9.53778e+06 |      500 | create_task         |           2442 |
| 13 | VALIDATE_TASK                                         |               406 |         4773     |            8784 |             605 |             5595.5 |      5.43322e+06 |      500 | create_task         |           2442 |
| 14 | VALIDATE_TEAM                                         |               408 |        22484.8   |           26812 |           16042 |            22588.5 |      6.88696e+06 |      500 | create_task         |           2442 |
| 15 | VALIDATE_USER                                         |               408 |        16270.4   |           19238 |            6639 |            16201.5 |      2.02499e+06 |      500 | create_task         |           2442 |
| 16 | CREATE_USER_PREFERENCE                                |               468 |       110035     |          156685 |            6869 |           112423   |      7.18206e+08 |     1000 | create_user_profile |           1404 |
| 17 | CREATE_USER_PROFILE                                   |               468 |        80703.1   |          114157 |            3532 |            84184.5 |      4.43513e+08 |     1000 | create_user_profile |           1404 |
| 18 | CREATE_FILE_OBJECT                                    |               418 |        70196.9   |           91247 |            6077 |            69758.5 |      2.00832e+08 |     1000 | create_file_object  |           1254 |
| 19 | VALIDATE_FILE_OBJECT                                  |               419 |        13711.7   |           36281 |             654 |             5535   |      1.39916e+08 |     1000 | create_file_object  |           1254 |
| 20 | CREATE_DEFAULT_TEAM_AND_ADD_INITIAL_DEFAULT_TEAM_USER |               258 |        84602.9   |          109294 |           59622 |            83409   |      2.24372e+08 |     1000 | create_organization |           1290 |
| 21 | CREATE_ORGANIZATION_AND_ADD_INITIAL_ORGANIZATION_USER |               258 |        50790.1   |           58424 |           39181 |            49276.5 |      3.31845e+07 |     1000 | create_organization |           1290 |
| 22 | VALIDATE_ORGANIZATION                                 |               258 |         5208.91  |           10363 |             814 |             4204   |      8.59648e+06 |     1000 | create_organization |           1290 |
| 23 | VALIDATE_USER                                         |               258 |        33735     |           37987 |           11827 |            34693   |      1.38818e+07 |     1000 | create_organization |           1290 |
| 24 | CREATE_TEAM_AND_ADD_INITIAL_TEAM_USER                 |               123 |        71382.5   |           93732 |           31943 |            77006   |      2.2754e+08  |     1000 | create_team         |            496 |
| 25 | VALIDATE_ORGANIZATION_AND_ORGANIZATION_USER_EXIST     |               125 |        45625     |           52304 |            5118 |            49086   |      8.2327e+07  |     1000 | create_team         |            496 |
| 26 | VALIDATE_TEAM                                         |               125 |         2869.59  |            5187 |             612 |             3072   | 700288           |     1000 | create_team         |            496 |
| 27 | CREATE_TASK_AND_ATTACH_FILE_OBJECT                    |               116 |        81818     |           92734 |           52503 |            82800.5 |      5.27466e+07 |     1000 | create_task         |            702 |
| 28 | VALIDATE_FILE_OBJECT                                  |               116 |        53602.8   |           56892 |           41834 |            53464   |      4.1968e+06  |     1000 | create_task         |            702 |
| 29 | VALIDATE_TASK                                         |               118 |         3377.33  |            8451 |            1430 |             2979   |      1.77186e+06 |     1000 | create_task         |            702 |
| 30 | VALIDATE_TEAM                                         |               118 |        40578     |           43977 |           31353 |            39923   |      3.6692e+06  |     1000 | create_task         |            702 |
| 31 | VALIDATE_USER                                         |               118 |        29988.4   |           32724 |            8822 |            30273.5 |      9.96994e+06 |     1000 | create_task         |            702 |
| 32 | CREATE_USER_PREFERENCE                                |               333 |        11142.7   |           16229 |            5204 |            11391   |      1.11281e+07 |      300 | create_user_profile |            999 |
| 33 | CREATE_USER_PROFILE                                   |               333 |         7475.54  |           12067 |            2151 |             7272   |      5.60923e+06 |      300 | create_user_profile |            999 |
| 34 | CREATE_FILE_OBJECT                                    |               322 |        11380.5   |           16331 |            3635 |            11271   |      2.78038e+06 |      300 | create_file_object  |            966 |
| 35 | VALIDATE_FILE_OBJECT                                  |               322 |         3487.31  |            7576 |             742 |             3278.5 |      2.65192e+06 |      300 | create_file_object  |            966 |
| 36 | CREATE_DEFAULT_TEAM_AND_ADD_INITIAL_DEFAULT_TEAM_USER |                86 |        18700.1   |           21297 |           16281 |            18141.5 |      2.43873e+06 |      300 | create_organization |            435 |
| 37 | CREATE_ORGANIZATION_AND_ADD_INITIAL_ORGANIZATION_USER |                87 |        13784.7   |           14748 |           11877 |            13831   | 556741           |      300 | create_organization |            435 |
| 38 | VALIDATE_ORGANIZATION                                 |                88 |         1606.41  |            2742 |             694 |             1692   | 171285           |      300 | create_organization |            435 |
| 39 | VALIDATE_USER                                         |                88 |         9772.91  |           10473 |            8040 |             9671.5 | 195322           |      300 | create_organization |            435 |
| 40 | CREATE_TEAM_AND_ADD_INITIAL_TEAM_USER                 |               219 |        17252.9   |           20408 |           11464 |            18065   |      5.05767e+06 |      300 | create_team         |            880 |
| 41 | VALIDATE_ORGANIZATION_AND_ORGANIZATION_USER_EXIST     |               221 |         9681.76  |           13875 |            7907 |             9462   | 745287           |      300 | create_team         |            880 |
| 42 | VALIDATE_TEAM                                         |               221 |         2238.93  |            4658 |             516 |             2232   | 856141           |      300 | create_team         |            880 |
| 43 | CREATE_TASK_AND_ATTACH_FILE_OBJECT                    |               233 |        24159     |           26950 |           19040 |            24426   |      2.43045e+06 |      300 | create_task         |           1398 |
| 44 | VALIDATE_FILE_OBJECT                                  |               233 |        18471.6   |           19636 |           15220 |            18629   | 382378           |      300 | create_task         |           1398 |
| 45 | VALIDATE_TASK                                         |               233 |         3210.51  |            5634 |             945 |             3223   |      1.31254e+06 |      300 | create_task         |           1398 |
| 46 | VALIDATE_TEAM                                         |               233 |        13929.4   |           15109 |           11713 |            13970   | 304520           |      300 | create_task         |           1398 |
| 47 | VALIDATE_USER                                         |               233 |         9694.31  |           10666 |            7496 |             9705   | 184934           |      300 | create_task         |           1398 |
| 48 | CREATE_USER_PREFERENCE                                |               498 |         6799.01  |            9775 |            3560 |             6833   |      1.68261e+06 |      100 | create_user_profile |           1494 |
| 49 | CREATE_USER_PROFILE                                   |               498 |         4061.36  |            6680 |            2235 |             3946   | 715804           |      100 | create_user_profile |           1494 |
| 50 | CREATE_FILE_OBJECT                                    |               483 |         5736.07  |            7956 |            2419 |             5691   | 833049           |      100 | create_file_object  |           1449 |
| 51 | VALIDATE_FILE_OBJECT                                  |               483 |         2057.17  |            3891 |             274 |             1961   | 694481           |      100 | create_file_object  |           1449 |
| 52 | CREATE_DEFAULT_TEAM_AND_ADD_INITIAL_DEFAULT_TEAM_USER |               472 |        10935.8   |           13200 |            7302 |            10975.5 |      1.3162e+06  |      100 | create_organization |           2360 |
| 53 | CREATE_ORGANIZATION_AND_ADD_INITIAL_ORGANIZATION_USER |               472 |         8151.77  |           10633 |            5363 |             8155   | 547202           |      100 | create_organization |           2360 |
| 54 | VALIDATE_ORGANIZATION                                 |               472 |         2861.27  |            5018 |             384 |             2952.5 |      1.12102e+06 |      100 | create_organization |           2360 |
| 55 | VALIDATE_USER                                         |               472 |         5898.4   |            7173 |            3118 |             5941.5 | 366349           |      100 | create_organization |           2360 |
| 56 | CREATE_TEAM_AND_ADD_INITIAL_TEAM_USER                 |               528 |         8102.99  |           11280 |            5109 |             8001.5 |      1.50772e+06 |      100 | create_team         |           2112 |
| 57 | VALIDATE_ORGANIZATION_AND_ORGANIZATION_USER_EXIST     |               528 |         5340.44  |            7490 |            2185 |             5288   | 818383           |      100 | create_team         |           2112 |
| 58 | VALIDATE_TEAM                                         |               528 |         2236.49  |            4957 |              63 |             2006   | 927426           |      100 | create_team         |           2112 |
| 59 | CREATE_TASK_AND_ATTACH_FILE_OBJECT                    |               547 |        12949.4   |           15800 |            9472 |            13010   |      1.89572e+06 |      100 | create_task         |           3294 |
| 60 | VALIDATE_FILE_OBJECT                                  |               549 |        10224.4   |           12860 |            7552 |            10213   | 941031           |      100 | create_task         |           3294 |
| 61 | VALIDATE_TASK                                         |               550 |         2456.29  |            5037 |             259 |             2315.5 | 881651           |      100 | create_task         |           3294 |
| 62 | VALIDATE_TEAM                                         |               551 |         7916.32  |            9909 |            5784 |             7907   | 820838           |      100 | create_task         |           3294 |
| 63 | VALIDATE_USER                                         |               550 |         5660.21  |            7498 |            3232 |             5672.5 | 627279           |      100 | create_task         |           3294 |
| 64 | CREATE_USER_PREFERENCE                                |                70 |         3334.79  |            4200 |            2811 |             3266.5 | 119800           |       10 | create_user_profile |            213 |
| 65 | CREATE_USER_PROFILE                                   |                72 |         2173.17  |            2744 |            1797 |             2198.5 |  32865.5         |       10 | create_user_profile |            213 |
| 66 | CREATE_FILE_OBJECT                                    |                60 |         2182.47  |            3308 |            1653 |             2100   | 199806           |       10 | create_file_object  |            180 |
| 67 | VALIDATE_FILE_OBJECT                                  |                60 |         1130.43  |            1519 |             666 |             1116.5 |  63464.8         |       10 | create_file_object  |            180 |
| 68 | CREATE_DEFAULT_TEAM_AND_ADD_INITIAL_DEFAULT_TEAM_USER |                55 |         4777.8   |            6701 |            3679 |             4626   | 724535           |       10 | create_organization |            285 |
| 69 | CREATE_ORGANIZATION_AND_ADD_INITIAL_ORGANIZATION_USER |                58 |         3471.78  |            5215 |            2657 |             3254   | 492534           |       10 | create_organization |            285 |
| 70 | VALIDATE_ORGANIZATION                                 |                57 |         1411.46  |            1904 |             713 |             1340   |  97410.1         |       10 | create_organization |            285 |
| 71 | VALIDATE_USER                                         |                59 |         2323.81  |            3683 |            1664 |             2239   | 312077           |       10 | create_organization |            285 |
| 72 | CREATE_TEAM_AND_ADD_INITIAL_TEAM_USER                 |                50 |         3713.5   |            5147 |            2728 |             3599   | 515571           |       10 | create_team         |            200 |
| 73 | VALIDATE_ORGANIZATION_AND_ORGANIZATION_USER_EXIST     |                50 |         2181.3   |            3207 |            1560 |             2173.5 | 214171           |       10 | create_team         |            200 |
| 74 | VALIDATE_TEAM                                         |                50 |         1268.14  |            1722 |             701 |             1297.5 |  59885.5         |       10 | create_team         |            200 |
| 75 | CREATE_TASK_AND_ATTACH_FILE_OBJECT                    |                50 |         5935.06  |            6683 |            5305 |             5923   | 161389           |       10 | create_task         |            300 |
| 76 | VALIDATE_FILE_OBJECT                                  |                50 |         4778.14  |            5282 |            4207 |             4714.5 | 105454           |       10 | create_task         |            300 |
| 77 | VALIDATE_TASK                                         |                50 |         1317.22  |            1778 |             697 |             1327.5 | 104325           |       10 | create_task         |            300 |
| 78 | VALIDATE_TEAM                                         |                50 |         3529.12  |            4402 |            2624 |             3672   | 294572           |       10 | create_task         |            300 |
| 79 | VALIDATE_USER                                         |                50 |         2330.6   |            2884 |            1616 |             2167   | 173459           |       10 | create_task         |            300 |
| 80 | CREATE_USER_PREFERENCE                                |                94 |         3077.52  |            5168 |            2249 |             2899   | 403025           |        1 | create_user_profile |            282 |
| 81 | CREATE_USER_PROFILE                                   |                94 |         2046.01  |            3652 |            1620 |             1893   | 125918           |        1 | create_user_profile |            282 |
| 82 | CREATE_FILE_OBJECT                                    |                94 |         2028.68  |            3677 |            1524 |             1835   | 204813           |        1 | create_file_object  |            282 |
| 83 | VALIDATE_FILE_OBJECT                                  |                94 |          987.649 |            1852 |             382 |              824   | 105407           |        1 | create_file_object  |            282 |
| 84 | CREATE_DEFAULT_TEAM_AND_ADD_INITIAL_DEFAULT_TEAM_USER |                79 |         4133.38  |            5751 |            3156 |             4078   | 235512           |        1 | create_organization |            395 |
| 85 | CREATE_ORGANIZATION_AND_ADD_INITIAL_ORGANIZATION_USER |                79 |         3055.29  |            4336 |            2172 |             3062   | 132440           |        1 | create_organization |            395 |
| 86 | VALIDATE_ORGANIZATION                                 |                79 |          996.063 |            1737 |             508 |             1018   |  93636.1         |        1 | create_organization |            395 |
| 87 | VALIDATE_USER                                         |                79 |         1982.2   |            2830 |            1170 |             2031   | 115945           |        1 | create_organization |            395 |
| 88 | CREATE_TEAM_AND_ADD_INITIAL_TEAM_USER                 |                64 |         3132     |            4306 |            2004 |             3109.5 | 188269           |        1 | create_team         |            256 |
| 89 | VALIDATE_ORGANIZATION_AND_ORGANIZATION_USER_EXIST     |                64 |         2030.83  |            2739 |             889 |             2028.5 | 142548           |        1 | create_team         |            256 |
| 90 | VALIDATE_TEAM                                         |                64 |          927.672 |            1743 |             285 |              970   | 110252           |        1 | create_team         |            256 |
| 91 | CREATE_TASK_AND_ATTACH_FILE_OBJECT                    |                60 |         5011.53  |            7055 |            3107 |             4915.5 |      1.03587e+06 |        1 | create_task         |            360 |
| 92 | VALIDATE_FILE_OBJECT                                  |                60 |         3953.8   |            6070 |            1792 |             3941.5 |      1.11735e+06 |        1 | create_task         |            360 |
| 93 | VALIDATE_TASK                                         |                60 |          921.817 |            1462 |             252 |              961   | 133629           |        1 | create_task         |            360 |
| 94 | VALIDATE_TEAM                                         |                60 |         2893.97  |            4488 |            1224 |             2858   | 642698           |        1 | create_task         |            360 |
| 95 | VALIDATE_USER                                         |                60 |         1918.2   |            3078 |             908 |             1880.5 | 413892           |        1 | create_task         |            360 |