/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
$(document).ready(function() {

    $(".click-title").mouseenter( function(    e){
        e.preventDefault();
        this.style.cursor="pointer";
    });
    $(".click-title").mousedown( function(event){
        event.preventDefault();
    });

    // Ugly code while this script is shared among several pages
    try{
        refreshHitsPerSecond(true);
    } catch(e){}
    try{
        refreshResponseTimeOverTime(true);
    } catch(e){}
    try{
        refreshResponseTimePercentiles();
    } catch(e){}
});


var responseTimePercentilesInfos = {
        data: {"result": {"minY": 3769.0, "minX": 0.0, "maxY": 30114.0, "series": [{"data": [[0.0, 3769.0], [0.1, 3769.0], [0.2, 3769.0], [0.3, 3769.0], [0.4, 3769.0], [0.5, 3769.0], [0.6, 3769.0], [0.7, 3769.0], [0.8, 3769.0], [0.9, 3769.0], [1.0, 3769.0], [1.1, 3769.0], [1.2, 3769.0], [1.3, 3769.0], [1.4, 3769.0], [1.5, 3769.0], [1.6, 3769.0], [1.7, 3769.0], [1.8, 3769.0], [1.9, 3769.0], [2.0, 3769.0], [2.1, 3769.0], [2.2, 3769.0], [2.3, 4126.0], [2.4, 4126.0], [2.5, 4126.0], [2.6, 4126.0], [2.7, 4126.0], [2.8, 4126.0], [2.9, 4126.0], [3.0, 4126.0], [3.1, 4126.0], [3.2, 4126.0], [3.3, 4126.0], [3.4, 4126.0], [3.5, 4126.0], [3.6, 4126.0], [3.7, 4126.0], [3.8, 4126.0], [3.9, 4126.0], [4.0, 4126.0], [4.1, 4126.0], [4.2, 4126.0], [4.3, 4126.0], [4.4, 4126.0], [4.5, 4436.0], [4.6, 4436.0], [4.7, 4436.0], [4.8, 4436.0], [4.9, 4436.0], [5.0, 4436.0], [5.1, 4436.0], [5.2, 4436.0], [5.3, 4436.0], [5.4, 4436.0], [5.5, 4436.0], [5.6, 4436.0], [5.7, 4436.0], [5.8, 4436.0], [5.9, 4436.0], [6.0, 4436.0], [6.1, 4436.0], [6.2, 4436.0], [6.3, 4436.0], [6.4, 4436.0], [6.5, 4436.0], [6.6, 4436.0], [6.7, 4648.0], [6.8, 4648.0], [6.9, 4648.0], [7.0, 4648.0], [7.1, 4648.0], [7.2, 4648.0], [7.3, 4648.0], [7.4, 4648.0], [7.5, 4648.0], [7.6, 4648.0], [7.7, 4648.0], [7.8, 4648.0], [7.9, 4648.0], [8.0, 4648.0], [8.1, 4648.0], [8.2, 4648.0], [8.3, 4648.0], [8.4, 4648.0], [8.5, 4648.0], [8.6, 4648.0], [8.7, 4648.0], [8.8, 4648.0], [8.9, 4659.0], [9.0, 4659.0], [9.1, 4659.0], [9.2, 4659.0], [9.3, 4659.0], [9.4, 4659.0], [9.5, 4659.0], [9.6, 4659.0], [9.7, 4659.0], [9.8, 4659.0], [9.9, 4659.0], [10.0, 4659.0], [10.1, 4659.0], [10.2, 4659.0], [10.3, 4659.0], [10.4, 4659.0], [10.5, 4659.0], [10.6, 4659.0], [10.7, 4659.0], [10.8, 4659.0], [10.9, 4659.0], [11.0, 4659.0], [11.1, 4659.0], [11.2, 4771.0], [11.3, 4771.0], [11.4, 4771.0], [11.5, 4771.0], [11.6, 4771.0], [11.7, 4771.0], [11.8, 4771.0], [11.9, 4771.0], [12.0, 4771.0], [12.1, 4771.0], [12.2, 4771.0], [12.3, 4771.0], [12.4, 4771.0], [12.5, 4771.0], [12.6, 4771.0], [12.7, 4771.0], [12.8, 4771.0], [12.9, 4771.0], [13.0, 4771.0], [13.1, 4771.0], [13.2, 4771.0], [13.3, 4771.0], [13.4, 5498.0], [13.5, 5498.0], [13.6, 5498.0], [13.7, 5498.0], [13.8, 5498.0], [13.9, 5498.0], [14.0, 5498.0], [14.1, 5498.0], [14.2, 5498.0], [14.3, 5498.0], [14.4, 5498.0], [14.5, 5498.0], [14.6, 5498.0], [14.7, 5498.0], [14.8, 5498.0], [14.9, 5498.0], [15.0, 5498.0], [15.1, 5498.0], [15.2, 5498.0], [15.3, 5498.0], [15.4, 5498.0], [15.5, 5498.0], [15.6, 5503.0], [15.7, 5503.0], [15.8, 5503.0], [15.9, 5503.0], [16.0, 5503.0], [16.1, 5503.0], [16.2, 5503.0], [16.3, 5503.0], [16.4, 5503.0], [16.5, 5503.0], [16.6, 5503.0], [16.7, 5503.0], [16.8, 5503.0], [16.9, 5503.0], [17.0, 5503.0], [17.1, 5503.0], [17.2, 5503.0], [17.3, 5503.0], [17.4, 5503.0], [17.5, 5503.0], [17.6, 5503.0], [17.7, 5503.0], [17.8, 5641.0], [17.9, 5641.0], [18.0, 5641.0], [18.1, 5641.0], [18.2, 5641.0], [18.3, 5641.0], [18.4, 5641.0], [18.5, 5641.0], [18.6, 5641.0], [18.7, 5641.0], [18.8, 5641.0], [18.9, 5641.0], [19.0, 5641.0], [19.1, 5641.0], [19.2, 5641.0], [19.3, 5641.0], [19.4, 5641.0], [19.5, 5641.0], [19.6, 5641.0], [19.7, 5641.0], [19.8, 5641.0], [19.9, 5641.0], [20.0, 6158.0], [20.1, 6158.0], [20.2, 6158.0], [20.3, 6158.0], [20.4, 6158.0], [20.5, 6158.0], [20.6, 6158.0], [20.7, 6158.0], [20.8, 6158.0], [20.9, 6158.0], [21.0, 6158.0], [21.1, 6158.0], [21.2, 6158.0], [21.3, 6158.0], [21.4, 6158.0], [21.5, 6158.0], [21.6, 6158.0], [21.7, 6158.0], [21.8, 6158.0], [21.9, 6158.0], [22.0, 6158.0], [22.1, 6158.0], [22.2, 6158.0], [22.3, 8377.0], [22.4, 8377.0], [22.5, 8377.0], [22.6, 8377.0], [22.7, 8377.0], [22.8, 8377.0], [22.9, 8377.0], [23.0, 8377.0], [23.1, 8377.0], [23.2, 8377.0], [23.3, 8377.0], [23.4, 8377.0], [23.5, 8377.0], [23.6, 8377.0], [23.7, 8377.0], [23.8, 8377.0], [23.9, 8377.0], [24.0, 8377.0], [24.1, 8377.0], [24.2, 8377.0], [24.3, 8377.0], [24.4, 8377.0], [24.5, 9079.0], [24.6, 9079.0], [24.7, 9079.0], [24.8, 9079.0], [24.9, 9079.0], [25.0, 9079.0], [25.1, 9079.0], [25.2, 9079.0], [25.3, 9079.0], [25.4, 9079.0], [25.5, 9079.0], [25.6, 9079.0], [25.7, 9079.0], [25.8, 9079.0], [25.9, 9079.0], [26.0, 9079.0], [26.1, 9079.0], [26.2, 9079.0], [26.3, 9079.0], [26.4, 9079.0], [26.5, 9079.0], [26.6, 9079.0], [26.7, 9902.0], [26.8, 9902.0], [26.9, 9902.0], [27.0, 9902.0], [27.1, 9902.0], [27.2, 9902.0], [27.3, 9902.0], [27.4, 9902.0], [27.5, 9902.0], [27.6, 9902.0], [27.7, 9902.0], [27.8, 9902.0], [27.9, 9902.0], [28.0, 9902.0], [28.1, 9902.0], [28.2, 9902.0], [28.3, 9902.0], [28.4, 9902.0], [28.5, 9902.0], [28.6, 9902.0], [28.7, 9902.0], [28.8, 9902.0], [28.9, 10827.0], [29.0, 10827.0], [29.1, 10827.0], [29.2, 10827.0], [29.3, 10827.0], [29.4, 10827.0], [29.5, 10827.0], [29.6, 10827.0], [29.7, 10827.0], [29.8, 10827.0], [29.9, 10827.0], [30.0, 10827.0], [30.1, 10827.0], [30.2, 10827.0], [30.3, 10827.0], [30.4, 10827.0], [30.5, 10827.0], [30.6, 10827.0], [30.7, 10827.0], [30.8, 10827.0], [30.9, 10827.0], [31.0, 10827.0], [31.1, 10827.0], [31.2, 10964.0], [31.3, 10964.0], [31.4, 10964.0], [31.5, 10964.0], [31.6, 10964.0], [31.7, 10964.0], [31.8, 10964.0], [31.9, 10964.0], [32.0, 10964.0], [32.1, 10964.0], [32.2, 10964.0], [32.3, 10964.0], [32.4, 10964.0], [32.5, 10964.0], [32.6, 10964.0], [32.7, 10964.0], [32.8, 10964.0], [32.9, 10964.0], [33.0, 10964.0], [33.1, 10964.0], [33.2, 10964.0], [33.3, 10964.0], [33.4, 11618.0], [33.5, 11618.0], [33.6, 11618.0], [33.7, 11618.0], [33.8, 11618.0], [33.9, 11618.0], [34.0, 11618.0], [34.1, 11618.0], [34.2, 11618.0], [34.3, 11618.0], [34.4, 11618.0], [34.5, 11618.0], [34.6, 11618.0], [34.7, 11618.0], [34.8, 11618.0], [34.9, 11618.0], [35.0, 11618.0], [35.1, 11618.0], [35.2, 11618.0], [35.3, 11618.0], [35.4, 11618.0], [35.5, 11618.0], [35.6, 11963.0], [35.7, 11963.0], [35.8, 11963.0], [35.9, 11963.0], [36.0, 11963.0], [36.1, 11963.0], [36.2, 11963.0], [36.3, 11963.0], [36.4, 11963.0], [36.5, 11963.0], [36.6, 11963.0], [36.7, 11963.0], [36.8, 11963.0], [36.9, 11963.0], [37.0, 11963.0], [37.1, 11963.0], [37.2, 11963.0], [37.3, 11963.0], [37.4, 11963.0], [37.5, 11963.0], [37.6, 11963.0], [37.7, 11963.0], [37.8, 12269.0], [37.9, 12269.0], [38.0, 12269.0], [38.1, 12269.0], [38.2, 12269.0], [38.3, 12269.0], [38.4, 12269.0], [38.5, 12269.0], [38.6, 12269.0], [38.7, 12269.0], [38.8, 12269.0], [38.9, 12269.0], [39.0, 12269.0], [39.1, 12269.0], [39.2, 12269.0], [39.3, 12269.0], [39.4, 12269.0], [39.5, 12269.0], [39.6, 12269.0], [39.7, 12269.0], [39.8, 12269.0], [39.9, 12269.0], [40.0, 12748.0], [40.1, 12748.0], [40.2, 12748.0], [40.3, 12748.0], [40.4, 12748.0], [40.5, 12748.0], [40.6, 12748.0], [40.7, 12748.0], [40.8, 12748.0], [40.9, 12748.0], [41.0, 12748.0], [41.1, 12748.0], [41.2, 12748.0], [41.3, 12748.0], [41.4, 12748.0], [41.5, 12748.0], [41.6, 12748.0], [41.7, 12748.0], [41.8, 12748.0], [41.9, 12748.0], [42.0, 12748.0], [42.1, 12748.0], [42.2, 12748.0], [42.3, 12927.0], [42.4, 12927.0], [42.5, 12927.0], [42.6, 12927.0], [42.7, 12927.0], [42.8, 12927.0], [42.9, 12927.0], [43.0, 12927.0], [43.1, 12927.0], [43.2, 12927.0], [43.3, 12927.0], [43.4, 12927.0], [43.5, 12927.0], [43.6, 12927.0], [43.7, 12927.0], [43.8, 12927.0], [43.9, 12927.0], [44.0, 12927.0], [44.1, 12927.0], [44.2, 12927.0], [44.3, 12927.0], [44.4, 12927.0], [44.5, 13358.0], [44.6, 13358.0], [44.7, 13358.0], [44.8, 13358.0], [44.9, 13358.0], [45.0, 13358.0], [45.1, 13358.0], [45.2, 13358.0], [45.3, 13358.0], [45.4, 13358.0], [45.5, 13358.0], [45.6, 13358.0], [45.7, 13358.0], [45.8, 13358.0], [45.9, 13358.0], [46.0, 13358.0], [46.1, 13358.0], [46.2, 13358.0], [46.3, 13358.0], [46.4, 13358.0], [46.5, 13358.0], [46.6, 13358.0], [46.7, 13594.0], [46.8, 13594.0], [46.9, 13594.0], [47.0, 13594.0], [47.1, 13594.0], [47.2, 13594.0], [47.3, 13594.0], [47.4, 13594.0], [47.5, 13594.0], [47.6, 13594.0], [47.7, 13594.0], [47.8, 13594.0], [47.9, 13594.0], [48.0, 13594.0], [48.1, 13594.0], [48.2, 13594.0], [48.3, 13594.0], [48.4, 13594.0], [48.5, 13594.0], [48.6, 13594.0], [48.7, 13594.0], [48.8, 13594.0], [48.9, 13690.0], [49.0, 13690.0], [49.1, 13690.0], [49.2, 13690.0], [49.3, 13690.0], [49.4, 13690.0], [49.5, 13690.0], [49.6, 13690.0], [49.7, 13690.0], [49.8, 13690.0], [49.9, 13690.0], [50.0, 13690.0], [50.1, 13690.0], [50.2, 13690.0], [50.3, 13690.0], [50.4, 13690.0], [50.5, 13690.0], [50.6, 13690.0], [50.7, 13690.0], [50.8, 13690.0], [50.9, 13690.0], [51.0, 13690.0], [51.1, 13690.0], [51.2, 14867.0], [51.3, 14867.0], [51.4, 14867.0], [51.5, 14867.0], [51.6, 14867.0], [51.7, 14867.0], [51.8, 14867.0], [51.9, 14867.0], [52.0, 14867.0], [52.1, 14867.0], [52.2, 14867.0], [52.3, 14867.0], [52.4, 14867.0], [52.5, 14867.0], [52.6, 14867.0], [52.7, 14867.0], [52.8, 14867.0], [52.9, 14867.0], [53.0, 14867.0], [53.1, 14867.0], [53.2, 14867.0], [53.3, 14867.0], [53.4, 15342.0], [53.5, 15342.0], [53.6, 15342.0], [53.7, 15342.0], [53.8, 15342.0], [53.9, 15342.0], [54.0, 15342.0], [54.1, 15342.0], [54.2, 15342.0], [54.3, 15342.0], [54.4, 15342.0], [54.5, 15342.0], [54.6, 15342.0], [54.7, 15342.0], [54.8, 15342.0], [54.9, 15342.0], [55.0, 15342.0], [55.1, 15342.0], [55.2, 15342.0], [55.3, 15342.0], [55.4, 15342.0], [55.5, 15342.0], [55.6, 15565.0], [55.7, 15565.0], [55.8, 15565.0], [55.9, 15565.0], [56.0, 15565.0], [56.1, 15565.0], [56.2, 15565.0], [56.3, 15565.0], [56.4, 15565.0], [56.5, 15565.0], [56.6, 15565.0], [56.7, 15565.0], [56.8, 15565.0], [56.9, 15565.0], [57.0, 15565.0], [57.1, 15565.0], [57.2, 15565.0], [57.3, 15565.0], [57.4, 15565.0], [57.5, 15565.0], [57.6, 15565.0], [57.7, 15565.0], [57.8, 17233.0], [57.9, 17233.0], [58.0, 17233.0], [58.1, 17233.0], [58.2, 17233.0], [58.3, 17233.0], [58.4, 17233.0], [58.5, 17233.0], [58.6, 17233.0], [58.7, 17233.0], [58.8, 17233.0], [58.9, 17233.0], [59.0, 17233.0], [59.1, 17233.0], [59.2, 17233.0], [59.3, 17233.0], [59.4, 17233.0], [59.5, 17233.0], [59.6, 17233.0], [59.7, 17233.0], [59.8, 17233.0], [59.9, 17233.0], [60.0, 17564.0], [60.1, 17564.0], [60.2, 17564.0], [60.3, 17564.0], [60.4, 17564.0], [60.5, 17564.0], [60.6, 17564.0], [60.7, 17564.0], [60.8, 17564.0], [60.9, 17564.0], [61.0, 17564.0], [61.1, 17564.0], [61.2, 17564.0], [61.3, 17564.0], [61.4, 17564.0], [61.5, 17564.0], [61.6, 17564.0], [61.7, 17564.0], [61.8, 17564.0], [61.9, 17564.0], [62.0, 17564.0], [62.1, 17564.0], [62.2, 17564.0], [62.3, 17721.0], [62.4, 17721.0], [62.5, 17721.0], [62.6, 17721.0], [62.7, 17721.0], [62.8, 17721.0], [62.9, 17721.0], [63.0, 17721.0], [63.1, 17721.0], [63.2, 17721.0], [63.3, 17721.0], [63.4, 17721.0], [63.5, 17721.0], [63.6, 17721.0], [63.7, 17721.0], [63.8, 17721.0], [63.9, 17721.0], [64.0, 17721.0], [64.1, 17721.0], [64.2, 17721.0], [64.3, 17721.0], [64.4, 17721.0], [64.5, 18062.0], [64.6, 18062.0], [64.7, 18062.0], [64.8, 18062.0], [64.9, 18062.0], [65.0, 18062.0], [65.1, 18062.0], [65.2, 18062.0], [65.3, 18062.0], [65.4, 18062.0], [65.5, 18062.0], [65.6, 18062.0], [65.7, 18062.0], [65.8, 18062.0], [65.9, 18062.0], [66.0, 18062.0], [66.1, 18062.0], [66.2, 18062.0], [66.3, 18062.0], [66.4, 18062.0], [66.5, 18062.0], [66.6, 18062.0], [66.7, 18119.0], [66.8, 18119.0], [66.9, 18119.0], [67.0, 18119.0], [67.1, 18119.0], [67.2, 18119.0], [67.3, 18119.0], [67.4, 18119.0], [67.5, 18119.0], [67.6, 18119.0], [67.7, 18119.0], [67.8, 18119.0], [67.9, 18119.0], [68.0, 18119.0], [68.1, 18119.0], [68.2, 18119.0], [68.3, 18119.0], [68.4, 18119.0], [68.5, 18119.0], [68.6, 18119.0], [68.7, 18119.0], [68.8, 18119.0], [68.9, 18428.0], [69.0, 18428.0], [69.1, 18428.0], [69.2, 18428.0], [69.3, 18428.0], [69.4, 18428.0], [69.5, 18428.0], [69.6, 18428.0], [69.7, 18428.0], [69.8, 18428.0], [69.9, 18428.0], [70.0, 18428.0], [70.1, 18428.0], [70.2, 18428.0], [70.3, 18428.0], [70.4, 18428.0], [70.5, 18428.0], [70.6, 18428.0], [70.7, 18428.0], [70.8, 18428.0], [70.9, 18428.0], [71.0, 18428.0], [71.1, 18428.0], [71.2, 18429.0], [71.3, 18429.0], [71.4, 18429.0], [71.5, 18429.0], [71.6, 18429.0], [71.7, 18429.0], [71.8, 18429.0], [71.9, 18429.0], [72.0, 18429.0], [72.1, 18429.0], [72.2, 18429.0], [72.3, 18429.0], [72.4, 18429.0], [72.5, 18429.0], [72.6, 18429.0], [72.7, 18429.0], [72.8, 18429.0], [72.9, 18429.0], [73.0, 18429.0], [73.1, 18429.0], [73.2, 18429.0], [73.3, 18429.0], [73.4, 19956.0], [73.5, 19956.0], [73.6, 19956.0], [73.7, 19956.0], [73.8, 19956.0], [73.9, 19956.0], [74.0, 19956.0], [74.1, 19956.0], [74.2, 19956.0], [74.3, 19956.0], [74.4, 19956.0], [74.5, 19956.0], [74.6, 19956.0], [74.7, 19956.0], [74.8, 19956.0], [74.9, 19956.0], [75.0, 19956.0], [75.1, 19956.0], [75.2, 19956.0], [75.3, 19956.0], [75.4, 19956.0], [75.5, 19956.0], [75.6, 20011.0], [75.7, 20011.0], [75.8, 20011.0], [75.9, 20011.0], [76.0, 20011.0], [76.1, 20011.0], [76.2, 20011.0], [76.3, 20011.0], [76.4, 20011.0], [76.5, 20011.0], [76.6, 20011.0], [76.7, 20011.0], [76.8, 20011.0], [76.9, 20011.0], [77.0, 20011.0], [77.1, 20011.0], [77.2, 20011.0], [77.3, 20011.0], [77.4, 20011.0], [77.5, 20011.0], [77.6, 20011.0], [77.7, 20011.0], [77.8, 20080.0], [77.9, 20080.0], [78.0, 20080.0], [78.1, 20080.0], [78.2, 20080.0], [78.3, 20080.0], [78.4, 20080.0], [78.5, 20080.0], [78.6, 20080.0], [78.7, 20080.0], [78.8, 20080.0], [78.9, 20080.0], [79.0, 20080.0], [79.1, 20080.0], [79.2, 20080.0], [79.3, 20080.0], [79.4, 20080.0], [79.5, 20080.0], [79.6, 20080.0], [79.7, 20080.0], [79.8, 20080.0], [79.9, 20080.0], [80.0, 20080.0], [80.1, 20137.0], [80.2, 20137.0], [80.3, 20137.0], [80.4, 20137.0], [80.5, 20137.0], [80.6, 20137.0], [80.7, 20137.0], [80.8, 20137.0], [80.9, 20137.0], [81.0, 20137.0], [81.1, 20137.0], [81.2, 20137.0], [81.3, 20137.0], [81.4, 20137.0], [81.5, 20137.0], [81.6, 20137.0], [81.7, 20137.0], [81.8, 20137.0], [81.9, 20137.0], [82.0, 20137.0], [82.1, 20137.0], [82.2, 20137.0], [82.3, 21139.0], [82.4, 21139.0], [82.5, 21139.0], [82.6, 21139.0], [82.7, 21139.0], [82.8, 21139.0], [82.9, 21139.0], [83.0, 21139.0], [83.1, 21139.0], [83.2, 21139.0], [83.3, 21139.0], [83.4, 21139.0], [83.5, 21139.0], [83.6, 21139.0], [83.7, 21139.0], [83.8, 21139.0], [83.9, 21139.0], [84.0, 21139.0], [84.1, 21139.0], [84.2, 21139.0], [84.3, 21139.0], [84.4, 21139.0], [84.5, 22925.0], [84.6, 22925.0], [84.7, 22925.0], [84.8, 22925.0], [84.9, 22925.0], [85.0, 22925.0], [85.1, 22925.0], [85.2, 22925.0], [85.3, 22925.0], [85.4, 22925.0], [85.5, 22925.0], [85.6, 22925.0], [85.7, 22925.0], [85.8, 22925.0], [85.9, 22925.0], [86.0, 22925.0], [86.1, 22925.0], [86.2, 22925.0], [86.3, 22925.0], [86.4, 22925.0], [86.5, 22925.0], [86.6, 22925.0], [86.7, 23246.0], [86.8, 23246.0], [86.9, 23246.0], [87.0, 23246.0], [87.1, 23246.0], [87.2, 23246.0], [87.3, 23246.0], [87.4, 23246.0], [87.5, 23246.0], [87.6, 23246.0], [87.7, 23246.0], [87.8, 23246.0], [87.9, 23246.0], [88.0, 23246.0], [88.1, 23246.0], [88.2, 23246.0], [88.3, 23246.0], [88.4, 23246.0], [88.5, 23246.0], [88.6, 23246.0], [88.7, 23246.0], [88.8, 23246.0], [88.9, 24589.0], [89.0, 24589.0], [89.1, 24589.0], [89.2, 24589.0], [89.3, 24589.0], [89.4, 24589.0], [89.5, 24589.0], [89.6, 24589.0], [89.7, 24589.0], [89.8, 24589.0], [89.9, 24589.0], [90.0, 24589.0], [90.1, 24589.0], [90.2, 24589.0], [90.3, 24589.0], [90.4, 24589.0], [90.5, 24589.0], [90.6, 24589.0], [90.7, 24589.0], [90.8, 24589.0], [90.9, 24589.0], [91.0, 24589.0], [91.1, 24589.0], [91.2, 25918.0], [91.3, 25918.0], [91.4, 25918.0], [91.5, 25918.0], [91.6, 25918.0], [91.7, 25918.0], [91.8, 25918.0], [91.9, 25918.0], [92.0, 25918.0], [92.1, 25918.0], [92.2, 25918.0], [92.3, 25918.0], [92.4, 25918.0], [92.5, 25918.0], [92.6, 25918.0], [92.7, 25918.0], [92.8, 25918.0], [92.9, 25918.0], [93.0, 25918.0], [93.1, 25918.0], [93.2, 25918.0], [93.3, 25918.0], [93.4, 27730.0], [93.5, 27730.0], [93.6, 27730.0], [93.7, 27730.0], [93.8, 27730.0], [93.9, 27730.0], [94.0, 27730.0], [94.1, 27730.0], [94.2, 27730.0], [94.3, 27730.0], [94.4, 27730.0], [94.5, 27730.0], [94.6, 27730.0], [94.7, 27730.0], [94.8, 27730.0], [94.9, 27730.0], [95.0, 27730.0], [95.1, 27730.0], [95.2, 27730.0], [95.3, 27730.0], [95.4, 27730.0], [95.5, 27730.0], [95.6, 27868.0], [95.7, 27868.0], [95.8, 27868.0], [95.9, 27868.0], [96.0, 27868.0], [96.1, 27868.0], [96.2, 27868.0], [96.3, 27868.0], [96.4, 27868.0], [96.5, 27868.0], [96.6, 27868.0], [96.7, 27868.0], [96.8, 27868.0], [96.9, 27868.0], [97.0, 27868.0], [97.1, 27868.0], [97.2, 27868.0], [97.3, 27868.0], [97.4, 27868.0], [97.5, 27868.0], [97.6, 27868.0], [97.7, 27868.0], [97.8, 30114.0], [97.9, 30114.0], [98.0, 30114.0], [98.1, 30114.0], [98.2, 30114.0], [98.3, 30114.0], [98.4, 30114.0], [98.5, 30114.0], [98.6, 30114.0], [98.7, 30114.0], [98.8, 30114.0], [98.9, 30114.0], [99.0, 30114.0], [99.1, 30114.0], [99.2, 30114.0], [99.3, 30114.0], [99.4, 30114.0], [99.5, 30114.0], [99.6, 30114.0], [99.7, 30114.0], [99.8, 30114.0], [99.9, 30114.0], [100.0, 30114.0]], "isOverall": false, "label": "TC03-01 Ask RAG", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 100.0, "title": "Response Time Percentiles"}},
        getOptions: function() {
            return {
                series: {
                    points: { show: false }
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentiles'
                },
                xaxis: {
                    tickDecimals: 1,
                    axisLabel: "Percentiles",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Percentile value in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : %x.2 percentile was %y ms"
                },
                selection: { mode: "xy" },
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentiles"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesPercentiles"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesPercentiles"), dataset, prepareOverviewOptions(options));
        }
};

/**
 * @param elementId Id of element where we display message
 */
function setEmptyGraph(elementId) {
    $(function() {
        $(elementId).text("No graph series with filter="+seriesFilter);
    });
}

// Response times percentiles
function refreshResponseTimePercentiles() {
    var infos = responseTimePercentilesInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimePercentiles");
        return;
    }
    if (isGraph($("#flotResponseTimesPercentiles"))){
        infos.createGraph();
    } else {
        var choiceContainer = $("#choicesResponseTimePercentiles");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesPercentiles", "#overviewResponseTimesPercentiles");
        $('#bodyResponseTimePercentiles .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimeDistributionInfos = {
        data: {"result": {"minY": 1.0, "minX": 3700.0, "maxY": 2.0, "series": [{"data": [[8300.0, 1.0], [9000.0, 1.0], [9900.0, 1.0], [10900.0, 1.0], [10800.0, 1.0], [11600.0, 1.0], [11900.0, 1.0], [12200.0, 1.0], [12700.0, 1.0], [12900.0, 1.0], [13300.0, 1.0], [13500.0, 1.0], [13600.0, 1.0], [14800.0, 1.0], [15300.0, 1.0], [15500.0, 1.0], [17200.0, 1.0], [18400.0, 2.0], [18000.0, 1.0], [18100.0, 1.0], [17500.0, 1.0], [17700.0, 1.0], [20000.0, 2.0], [20100.0, 1.0], [19900.0, 1.0], [21100.0, 1.0], [23200.0, 1.0], [22900.0, 1.0], [24500.0, 1.0], [25900.0, 1.0], [27800.0, 1.0], [27700.0, 1.0], [30100.0, 1.0], [3700.0, 1.0], [4100.0, 1.0], [4600.0, 2.0], [4400.0, 1.0], [4700.0, 1.0], [5500.0, 1.0], [5400.0, 1.0], [5600.0, 1.0], [6100.0, 1.0]], "isOverall": false, "label": "TC03-01 Ask RAG", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 100, "maxX": 30100.0, "title": "Response Time Distribution"}},
        getOptions: function() {
            var granularity = this.data.result.granularity;
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    barWidth: this.data.result.granularity
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " responses for " + label + " were between " + xval + " and " + (xval + granularity) + " ms";
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimeDistribution"), prepareData(data.result.series, $("#choicesResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshResponseTimeDistribution() {
    var infos = responseTimeDistributionInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeDistribution");
        return;
    }
    if (isGraph($("#flotResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var syntheticResponseTimeDistributionInfos = {
        data: {"result": {"minY": 45.0, "minX": 2.0, "ticks": [[0, "Requests having \nresponse time <= 500ms"], [1, "Requests having \nresponse time > 500ms and <= 1,500ms"], [2, "Requests having \nresponse time > 1,500ms"], [3, "Requests in error"]], "maxY": 45.0, "series": [{"data": [], "color": "#9ACD32", "isOverall": false, "label": "Requests having \nresponse time <= 500ms", "isController": false}, {"data": [], "color": "yellow", "isOverall": false, "label": "Requests having \nresponse time > 500ms and <= 1,500ms", "isController": false}, {"data": [[2.0, 45.0]], "color": "orange", "isOverall": false, "label": "Requests having \nresponse time > 1,500ms", "isController": false}, {"data": [], "color": "#FF6347", "isOverall": false, "label": "Requests in error", "isController": false}], "supportsControllersDiscrimination": false, "maxX": 2.0, "title": "Synthetic Response Times Distribution"}},
        getOptions: function() {
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendSyntheticResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times ranges",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                    tickLength:0,
                    min:-0.5,
                    max:3.5
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    align: "center",
                    barWidth: 0.25,
                    fill:.75
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " " + label;
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            options.xaxis.ticks = data.result.ticks;
            $.plot($("#flotSyntheticResponseTimeDistribution"), prepareData(data.result.series, $("#choicesSyntheticResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshSyntheticResponseTimeDistribution() {
    var infos = syntheticResponseTimeDistributionInfos;
    prepareSeries(infos.data, true);
    if (isGraph($("#flotSyntheticResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerSyntheticResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var activeThreadsOverTimeInfos = {
        data: {"result": {"minY": 10.071428571428573, "minX": 1.77660528E12, "maxY": 11.352941176470587, "series": [{"data": [[1.77660534E12, 10.071428571428573], [1.77660528E12, 11.352941176470587]], "isOverall": false, "label": "TC-03 Chatbot RAG Flow", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.77660534E12, "title": "Active Threads Over Time"}},
        getOptions: function() {
            return {
                series: {
                    stack: true,
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 6,
                    show: true,
                    container: '#legendActiveThreadsOverTime'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                selection: {
                    mode: 'xy'
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : At %x there were %y active threads"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesActiveThreadsOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotActiveThreadsOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewActiveThreadsOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Active Threads Over Time
function refreshActiveThreadsOverTime(fixTimestamps) {
    var infos = activeThreadsOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotActiveThreadsOverTime"))) {
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesActiveThreadsOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotActiveThreadsOverTime", "#overviewActiveThreadsOverTime");
        $('#footerActiveThreadsOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var timeVsThreadsInfos = {
        data: {"result": {"minY": 3769.0, "minX": 1.0, "maxY": 24589.0, "series": [{"data": [[8.0, 7476.5], [2.0, 11618.0], [9.0, 16445.6], [11.0, 17942.0], [12.0, 14182.8], [3.0, 3769.0], [13.0, 12799.8], [14.0, 15362.714285714284], [15.0, 13158.428571428572], [4.0, 15288.5], [1.0, 24589.0], [5.0, 12269.0], [6.0, 22925.0], [7.0, 16063.25]], "isOverall": false, "label": "TC03-01 Ask RAG", "isController": false}, {"data": [[10.555555555555554, 14568.177777777777]], "isOverall": false, "label": "TC03-01 Ask RAG-Aggregated", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 15.0, "title": "Time VS Threads"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: { noColumns: 2,show: true, container: '#legendTimeVsThreads' },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s: At %x.2 active threads, Average response time was %y.2 ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesTimeVsThreads"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotTimesVsThreads"), dataset, options);
            // setup overview
            $.plot($("#overviewTimesVsThreads"), dataset, prepareOverviewOptions(options));
        }
};

// Time vs threads
function refreshTimeVsThreads(){
    var infos = timeVsThreadsInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTimeVsThreads");
        return;
    }
    if(isGraph($("#flotTimesVsThreads"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTimeVsThreads");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTimesVsThreads", "#overviewTimesVsThreads");
        $('#footerTimeVsThreads .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var bytesThroughputOverTimeInfos = {
        data : {"result": {"minY": 367.9166666666667, "minX": 1.77660528E12, "maxY": 2699.1666666666665, "series": [{"data": [[1.77660534E12, 2699.1666666666665], [1.77660528E12, 1601.2166666666667]], "isOverall": false, "label": "Bytes received per second", "isController": false}, {"data": [[1.77660534E12, 604.2333333333333], [1.77660528E12, 367.9166666666667]], "isOverall": false, "label": "Bytes sent per second", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.77660534E12, "title": "Bytes Throughput Over Time"}},
        getOptions : function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity) ,
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Bytes / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendBytesThroughputOverTime'
                },
                selection: {
                    mode: "xy"
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y"
                }
            };
        },
        createGraph : function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesBytesThroughputOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotBytesThroughputOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewBytesThroughputOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Bytes throughput Over Time
function refreshBytesThroughputOverTime(fixTimestamps) {
    var infos = bytesThroughputOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotBytesThroughputOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesBytesThroughputOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotBytesThroughputOverTime", "#overviewBytesThroughputOverTime");
        $('#footerBytesThroughputOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimesOverTimeInfos = {
        data: {"result": {"minY": 14485.0, "minX": 1.77660528E12, "maxY": 14705.176470588236, "series": [{"data": [[1.77660534E12, 14485.0], [1.77660528E12, 14705.176470588236]], "isOverall": false, "label": "TC03-01 Ask RAG", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.77660534E12, "title": "Response Time Over Time"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average response time was %y ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Times Over Time
function refreshResponseTimeOverTime(fixTimestamps) {
    var infos = responseTimesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotResponseTimesOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesOverTime", "#overviewResponseTimesOverTime");
        $('#footerResponseTimesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var latenciesOverTimeInfos = {
        data: {"result": {"minY": 14480.535714285716, "minX": 1.77660528E12, "maxY": 14701.882352941177, "series": [{"data": [[1.77660534E12, 14480.535714285716], [1.77660528E12, 14701.882352941177]], "isOverall": false, "label": "TC03-01 Ask RAG", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.77660534E12, "title": "Latencies Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response latencies in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendLatenciesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average latency was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesLatenciesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotLatenciesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewLatenciesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Latencies Over Time
function refreshLatenciesOverTime(fixTimestamps) {
    var infos = latenciesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyLatenciesOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotLatenciesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesLatenciesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotLatenciesOverTime", "#overviewLatenciesOverTime");
        $('#footerLatenciesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var connectTimeOverTimeInfos = {
        data: {"result": {"minY": 13.0, "minX": 1.77660528E12, "maxY": 88.05882352941175, "series": [{"data": [[1.77660534E12, 13.0], [1.77660528E12, 88.05882352941175]], "isOverall": false, "label": "TC03-01 Ask RAG", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.77660534E12, "title": "Connect Time Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getConnectTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average Connect Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendConnectTimeOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average connect time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesConnectTimeOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotConnectTimeOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewConnectTimeOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Connect Time Over Time
function refreshConnectTimeOverTime(fixTimestamps) {
    var infos = connectTimeOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyConnectTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotConnectTimeOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesConnectTimeOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotConnectTimeOverTime", "#overviewConnectTimeOverTime");
        $('#footerConnectTimeOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var responseTimePercentilesOverTimeInfos = {
        data: {"result": {"minY": 3769.0, "minX": 1.77660528E12, "maxY": 30114.0, "series": [{"data": [[1.77660534E12, 30114.0], [1.77660528E12, 27868.0]], "isOverall": false, "label": "Max", "isController": false}, {"data": [[1.77660534E12, 3769.0], [1.77660528E12, 4126.0]], "isOverall": false, "label": "Min", "isController": false}, {"data": [[1.77660534E12, 26099.200000000004], [1.77660528E12, 21683.199999999993]], "isOverall": false, "label": "90th percentile", "isController": false}, {"data": [[1.77660534E12, 30114.0], [1.77660528E12, 27868.0]], "isOverall": false, "label": "99th percentile", "isController": false}, {"data": [[1.77660534E12, 13219.0], [1.77660528E12, 14867.0]], "isOverall": false, "label": "Median", "isController": false}, {"data": [[1.77660534E12, 29041.199999999993], [1.77660528E12, 27868.0]], "isOverall": false, "label": "95th percentile", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.77660534E12, "title": "Response Time Percentiles Over Time (successful requests only)"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Response Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentilesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Response time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentilesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimePercentilesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimePercentilesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Time Percentiles Over Time
function refreshResponseTimePercentilesOverTime(fixTimestamps) {
    var infos = responseTimePercentilesOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotResponseTimePercentilesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimePercentilesOverTime", "#overviewResponseTimePercentilesOverTime");
        $('#footerResponseTimePercentilesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var responseTimeVsRequestInfos = {
    data: {"result": {"minY": 11395.0, "minX": 1.0, "maxY": 17564.0, "series": [{"data": [[2.0, 11395.0], [1.0, 17564.0], [4.0, 14516.0], [3.0, 15234.5]], "isOverall": false, "label": "Successes", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 4.0, "title": "Response Time Vs Request"}},
    getOptions: function() {
        return {
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Response Time in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: {
                noColumns: 2,
                show: true,
                container: '#legendResponseTimeVsRequest'
            },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median response time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesResponseTimeVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotResponseTimeVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewResponseTimeVsRequest"), dataset, prepareOverviewOptions(options));

    }
};

// Response Time vs Request
function refreshResponseTimeVsRequest() {
    var infos = responseTimeVsRequestInfos;
    prepareSeries(infos.data);
    if (isGraph($("#flotResponseTimeVsRequest"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeVsRequest");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimeVsRequest", "#overviewResponseTimeVsRequest");
        $('#footerResponseRimeVsRequest .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var latenciesVsRequestInfos = {
    data: {"result": {"minY": 11390.0, "minX": 1.0, "maxY": 17559.0, "series": [{"data": [[2.0, 11390.0], [1.0, 17559.0], [4.0, 14510.5], [3.0, 15232.0]], "isOverall": false, "label": "Successes", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 4.0, "title": "Latencies Vs Request"}},
    getOptions: function() {
        return{
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Latency in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: { noColumns: 2,show: true, container: '#legendLatencyVsRequest' },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median Latency time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesLatencyVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotLatenciesVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewLatenciesVsRequest"), dataset, prepareOverviewOptions(options));
    }
};

// Latencies vs Request
function refreshLatenciesVsRequest() {
        var infos = latenciesVsRequestInfos;
        prepareSeries(infos.data);
        if(isGraph($("#flotLatenciesVsRequest"))){
            infos.createGraph();
        }else{
            var choiceContainer = $("#choicesLatencyVsRequest");
            createLegend(choiceContainer, infos);
            infos.createGraph();
            setGraphZoomable("#flotLatenciesVsRequest", "#overviewLatenciesVsRequest");
            $('#footerLatenciesVsRequest .legendColorBox > div').each(function(i){
                $(this).clone().prependTo(choiceContainer.find("li").eq(i));
            });
        }
};

var hitsPerSecondInfos = {
        data: {"result": {"minY": 0.26666666666666666, "minX": 1.77660528E12, "maxY": 0.48333333333333334, "series": [{"data": [[1.77660534E12, 0.26666666666666666], [1.77660528E12, 0.48333333333333334]], "isOverall": false, "label": "hitsPerSecond", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.77660534E12, "title": "Hits Per Second"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of hits / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendHitsPerSecond"
                },
                selection: {
                    mode : 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y.2 hits/sec"
                }
            };
        },
        createGraph: function createGraph() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesHitsPerSecond"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotHitsPerSecond"), dataset, options);
            // setup overview
            $.plot($("#overviewHitsPerSecond"), dataset, prepareOverviewOptions(options));
        }
};

// Hits per second
function refreshHitsPerSecond(fixTimestamps) {
    var infos = hitsPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if (isGraph($("#flotHitsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesHitsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotHitsPerSecond", "#overviewHitsPerSecond");
        $('#footerHitsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var codesPerSecondInfos = {
        data: {"result": {"minY": 0.2833333333333333, "minX": 1.77660528E12, "maxY": 0.4666666666666667, "series": [{"data": [[1.77660534E12, 0.4666666666666667], [1.77660528E12, 0.2833333333333333]], "isOverall": false, "label": "200", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.77660534E12, "title": "Codes Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendCodesPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "Number of Response Codes %s at %x was %y.2 responses / sec"
                }
            };
        },
    createGraph: function() {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesCodesPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotCodesPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewCodesPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Codes per second
function refreshCodesPerSecond(fixTimestamps) {
    var infos = codesPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotCodesPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesCodesPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotCodesPerSecond", "#overviewCodesPerSecond");
        $('#footerCodesPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var transactionsPerSecondInfos = {
        data: {"result": {"minY": 0.2833333333333333, "minX": 1.77660528E12, "maxY": 0.4666666666666667, "series": [{"data": [[1.77660534E12, 0.4666666666666667], [1.77660528E12, 0.2833333333333333]], "isOverall": false, "label": "TC03-01 Ask RAG-success", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.77660534E12, "title": "Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTransactionsPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                }
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTransactionsPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTransactionsPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewTransactionsPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Transactions per second
function refreshTransactionsPerSecond(fixTimestamps) {
    var infos = transactionsPerSecondInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTransactionsPerSecond");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotTransactionsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTransactionsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTransactionsPerSecond", "#overviewTransactionsPerSecond");
        $('#footerTransactionsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var totalTPSInfos = {
        data: {"result": {"minY": 0.2833333333333333, "minX": 1.77660528E12, "maxY": 0.4666666666666667, "series": [{"data": [[1.77660534E12, 0.4666666666666667], [1.77660528E12, 0.2833333333333333]], "isOverall": false, "label": "Transaction-success", "isController": false}, {"data": [], "isOverall": false, "label": "Transaction-failure", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.77660534E12, "title": "Total Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTotalTPS"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                },
                colors: ["#9ACD32", "#FF6347"]
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTotalTPS"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTotalTPS"), dataset, options);
        // setup overview
        $.plot($("#overviewTotalTPS"), dataset, prepareOverviewOptions(options));
    }
};

// Total Transactions per second
function refreshTotalTPS(fixTimestamps) {
    var infos = totalTPSInfos;
    // We want to ignore seriesFilter
    prepareSeries(infos.data, false, true);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotTotalTPS"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTotalTPS");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTotalTPS", "#overviewTotalTPS");
        $('#footerTotalTPS .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

// Collapse the graph matching the specified DOM element depending the collapsed
// status
function collapse(elem, collapsed){
    if(collapsed){
        $(elem).parent().find(".fa-chevron-up").removeClass("fa-chevron-up").addClass("fa-chevron-down");
    } else {
        $(elem).parent().find(".fa-chevron-down").removeClass("fa-chevron-down").addClass("fa-chevron-up");
        if (elem.id == "bodyBytesThroughputOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshBytesThroughputOverTime(true);
            }
            document.location.href="#bytesThroughputOverTime";
        } else if (elem.id == "bodyLatenciesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesOverTime(true);
            }
            document.location.href="#latenciesOverTime";
        } else if (elem.id == "bodyCustomGraph") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCustomGraph(true);
            }
            document.location.href="#responseCustomGraph";
        } else if (elem.id == "bodyConnectTimeOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshConnectTimeOverTime(true);
            }
            document.location.href="#connectTimeOverTime";
        } else if (elem.id == "bodyResponseTimePercentilesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimePercentilesOverTime(true);
            }
            document.location.href="#responseTimePercentilesOverTime";
        } else if (elem.id == "bodyResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeDistribution();
            }
            document.location.href="#responseTimeDistribution" ;
        } else if (elem.id == "bodySyntheticResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshSyntheticResponseTimeDistribution();
            }
            document.location.href="#syntheticResponseTimeDistribution" ;
        } else if (elem.id == "bodyActiveThreadsOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshActiveThreadsOverTime(true);
            }
            document.location.href="#activeThreadsOverTime";
        } else if (elem.id == "bodyTimeVsThreads") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTimeVsThreads();
            }
            document.location.href="#timeVsThreads" ;
        } else if (elem.id == "bodyCodesPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCodesPerSecond(true);
            }
            document.location.href="#codesPerSecond";
        } else if (elem.id == "bodyTransactionsPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTransactionsPerSecond(true);
            }
            document.location.href="#transactionsPerSecond";
        } else if (elem.id == "bodyTotalTPS") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTotalTPS(true);
            }
            document.location.href="#totalTPS";
        } else if (elem.id == "bodyResponseTimeVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeVsRequest();
            }
            document.location.href="#responseTimeVsRequest";
        } else if (elem.id == "bodyLatenciesVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesVsRequest();
            }
            document.location.href="#latencyVsRequest";
        }
    }
}

/*
 * Activates or deactivates all series of the specified graph (represented by id parameter)
 * depending on checked argument.
 */
function toggleAll(id, checked){
    var placeholder = document.getElementById(id);

    var cases = $(placeholder).find(':checkbox');
    cases.prop('checked', checked);
    $(cases).parent().children().children().toggleClass("legend-disabled", !checked);

    var choiceContainer;
    if ( id == "choicesBytesThroughputOverTime"){
        choiceContainer = $("#choicesBytesThroughputOverTime");
        refreshBytesThroughputOverTime(false);
    } else if(id == "choicesResponseTimesOverTime"){
        choiceContainer = $("#choicesResponseTimesOverTime");
        refreshResponseTimeOverTime(false);
    }else if(id == "choicesResponseCustomGraph"){
        choiceContainer = $("#choicesResponseCustomGraph");
        refreshCustomGraph(false);
    } else if ( id == "choicesLatenciesOverTime"){
        choiceContainer = $("#choicesLatenciesOverTime");
        refreshLatenciesOverTime(false);
    } else if ( id == "choicesConnectTimeOverTime"){
        choiceContainer = $("#choicesConnectTimeOverTime");
        refreshConnectTimeOverTime(false);
    } else if ( id == "choicesResponseTimePercentilesOverTime"){
        choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        refreshResponseTimePercentilesOverTime(false);
    } else if ( id == "choicesResponseTimePercentiles"){
        choiceContainer = $("#choicesResponseTimePercentiles");
        refreshResponseTimePercentiles();
    } else if(id == "choicesActiveThreadsOverTime"){
        choiceContainer = $("#choicesActiveThreadsOverTime");
        refreshActiveThreadsOverTime(false);
    } else if ( id == "choicesTimeVsThreads"){
        choiceContainer = $("#choicesTimeVsThreads");
        refreshTimeVsThreads();
    } else if ( id == "choicesSyntheticResponseTimeDistribution"){
        choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        refreshSyntheticResponseTimeDistribution();
    } else if ( id == "choicesResponseTimeDistribution"){
        choiceContainer = $("#choicesResponseTimeDistribution");
        refreshResponseTimeDistribution();
    } else if ( id == "choicesHitsPerSecond"){
        choiceContainer = $("#choicesHitsPerSecond");
        refreshHitsPerSecond(false);
    } else if(id == "choicesCodesPerSecond"){
        choiceContainer = $("#choicesCodesPerSecond");
        refreshCodesPerSecond(false);
    } else if ( id == "choicesTransactionsPerSecond"){
        choiceContainer = $("#choicesTransactionsPerSecond");
        refreshTransactionsPerSecond(false);
    } else if ( id == "choicesTotalTPS"){
        choiceContainer = $("#choicesTotalTPS");
        refreshTotalTPS(false);
    } else if ( id == "choicesResponseTimeVsRequest"){
        choiceContainer = $("#choicesResponseTimeVsRequest");
        refreshResponseTimeVsRequest();
    } else if ( id == "choicesLatencyVsRequest"){
        choiceContainer = $("#choicesLatencyVsRequest");
        refreshLatenciesVsRequest();
    }
    var color = checked ? "black" : "#818181";
    if(choiceContainer != null) {
        choiceContainer.find("label").each(function(){
            this.style.color = color;
        });
    }
}

