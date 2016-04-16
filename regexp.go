//This for test rexexp in go vs perl
package main

import  (
        "fmt"
        "regexp"
        )

func main() {
        pat := `((.+? ){2}).*?\[SMSC\:(.*?)\] .*?\[ACT\:(.*?)\] .*?\[FID\:(.*?)\] .*?\[from\:(.*?)\] \[to\:(.*?)\] .*?\[msg\:\d+\:(.*?)\].*`
        line := "2016-04-15 00:39:16 Sent SMS [SMSC:OTSEG_New] [ACT:nemra1:end2end] [FID:dfd9ea7b-9313-43a2-93b4-44d0e48ac5b1] [from:feccfa] [to:201017391154] [msg:122:06310645063200200641064A0633062806480643003A0020200F00390039003000350038200F002E00200623063A06440642002006470630064700200627064406310633062706440629002006480623062F062E0644002006270644063106450632002006250644064900200641064A06330628064806430020] [META:?smpp_resp?] [udh:6:050003DB0201]"
        re := regexp.MustCompile(pat)
        res := re.FindAllStringSubmatch(line, -1)
        fmt.Println("%v ",res)
        fmt.Println("%v ",res[0])
        fmt.Println()
        fmt.Println("Date : %v ",res[0][1])
        //fmt.Println("%v ",res[0][2])
        fmt.Println("SMSC : %v ",res[0][3])
        fmt.Println("Account : %v ",res[0][4])
        fmt.Println("FID : %v ",res[0][5])
        fmt.Println("Sender : %v ",res[0][6])
        fmt.Println("To : %v ",res[0][7])
        fmt.Println("MSG : %v ",res[0][8])
}
