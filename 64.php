<?php

class gsql{

    public $g_dict=array(
            "77"=>"乾为天",
            "76"=>"天泽履",
            "75"=>"天火同人",
            "74"=>"天雷无妄",
            "73"=>"天风姤",
            "72"=>"天水讼",
            "71"=>"天山遁",
            "70"=>"天地否",
            "67"=>"泽天夬",
            "66"=>"兑为泽",
            "65"=>"泽火革",
            "64"=>"泽雷随",
            "63"=>"泽风大过",
            "62"=>"泽水困",
            "61"=>"泽山咸",
            "60"=>"泽地萃",
            "57"=>"火天大有",
            "56"=>"火泽睽",
            "55"=>"离为火",
            "54"=>"火雷噬嗑",
            "53"=>"火风鼎",
            "52"=>"火水未济",
            "51"=>"火山旅",
            "50"=>"火地晋",
            "47"=>"雷天大壮",
            "46"=>"雷泽归妹",
            "45"=>"雷火丰",
            "44"=>"震为雷",
            "43"=>"雷风恒",
            "42"=>"雷水解",
            "41"=>"雷山小过",
            "40"=>"雷地豫",
            "37"=>"风天小畜",
            "36"=>"风泽中孚",
            "35"=>"风火家人",
            "34"=>"风雷益",
            "33"=>"巽为风",
            "32"=>"风水涣",
            "31"=>"风山渐",
            "30"=>"风地观",
            "27"=>"水天需",
            "26"=>"水泽节",
            "25"=>"水火既济",
            "24"=>"水雷屯",
            "23"=>"水风井",
            "22"=>"坎为水",
            "21"=>"水山蹇",
            "20"=>"水地比",
            "17"=>"山天大畜",
            "16"=>"山泽损",
            "15"=>"山火贲",
            "14"=>"山雷颐",
            "13"=>"山风蛊",
            "12"=>"山水蒙",
            "11"=>"艮为山",
            "10"=>"山地剥",
            "07"=>"地天泰",
            "06"=>"地泽临",
            "05"=>"地火明夷",
            "04"=>"地雷复",
            "03"=>"地风升",
            "02"=>"地水师",
            "01"=>"地山谦",
            "00"=>"坤为地"
            );

    function gener_g($up,$down,$dong)
    {
        $ben= (string)$up.(string)$down;

        if($dong<=3){
            if(($down&(4>>($dong-1)))!=0)
                $down &= ~(4>>($dong-1));
            else
                $down |= (4>>($dong-1));
        }
        elseif($dong>3 and $dong<=6){
            $dong -= 3;
            if(($up&(4>>($dong-1)))!=0)
                $up &= ~(4>>($dong-1));
            else
                $up |= 4>>($dong-1);
        }
        $change = (string)$up.(string)$down;
        return array($ben,$change,$ben.$change);
    }


    function loop_g()
    {
        $up=7;
        $down=7;
    
        $servername="localhost";
        $username="root";
        $passwd="101";
        $database="zy_health_pred";
        $mdb = new mysqli($servername, $username, $passwd,$database);
        $sql = "set names utf8";
        if(!$mdb->query($sql)){
            echo $mdb->error;
            goto sql_fail;
        }

        $sql_i="insert into zyh (gcode,descr,diag) values(\"";
        $g=" ";
        for($up=7;$up>=0;$up--)
            for($down=7;$down>=0;$down--){
                for($dong=1;$dong<7;$dong++){
                    $g = $this->gener_g($up,$down,$dong);
                    $info = $this->g_dict[$g[0]]."->".$this->g_dict[$g[1]];
                    $sql = $sql_i.$g[2]."\"".","."\"".$info."\"".","."\"null\"".")";
                    
                    if(false==$mdb->query($sql)){
                        echo $mdb->error;
                        goto sql_fail;
                    }
                    $mdb->commit();
                    //echo $g[2]."  ";
                    //echo $info."\n";
                }
            }
    sql_fail:
        $mdb->close();

    }

//end class
}

$gua = new gsql();

$gua->loop_g();

?>

