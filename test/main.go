package main

import (
    "os"
    "fmt"
    "io/ioutil"
    "strconv"
    "encoding/json"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
)

type bitString string
func (b bitString) bitStringToBytes() []byte {
    var out []byte
    var str string

    for i := len(b); i > 0; i -= 8 {
        if i-8 < 0 {
            str = string(b[0:i])
        } else {
            str = string(b[i-8 : i])
        }
        v, err := strconv.ParseUint(str, 2, 8)
        if err != nil {
            panic(err)
        }
        out = append([]byte{byte(v)}, out...)
    }
    return out
}

func CreateAddrFilter() types.Bloom {
    var bloom types.Bloom
    jsonFile, err := os.Open("/Users/cyan/Desktop/projects/arb/new/data/addrs.json")
    if err != nil {
        fmt.Println(err)
    }
    defer jsonFile.Close()
    byteValue, err := ioutil.ReadAll(jsonFile)
    if err != nil {
        fmt.Println(err)
    }
    var addrs []common.Address
    json.Unmarshal(byteValue, &addrs)
    for i := 0; i < len(addrs); i ++ {
        bloom.Add(addrs[i].Bytes())
    }
    return bloom
}

func main() {
    bloom := CreateAddrFilter()

	addr := common.HexToAddress("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
	if types.BloomLookup(bloom, addr) {
		fmt.Printf("Yes")
	} else {
		fmt.Printf("No")
	}
}

