@staticmethod
def decodeCommand(rawStr:bytes):
    prefix =rawStr[0]
    match prefix:
        case 43: #+
            # RESP2 Simple string
            return rawStr[1:-2].decode("utf-8")
        case 45: #-
            #simple error
            return rawStr[1:-2].decode("utf-8")
        
        case 58: #[+|-] 
            #handles plus or minus ints no prefix means positive int
            if rawStr[1] == 43:
                return int(rawStr[2:-2].decode("utf-8"))
            elif rawStr[1] == 45:
                return int(rawStr[2:-2].decode("utf-8")) *-1
            else:
                return int(rawStr[1:-2].decode("utf-8"))
        # RESP2 Aggregate
        case 36: #$
            #"Bulk String (RESP2) schema: $<length>\r\n<data>\r\n"
            
            #finds index of the beginning of the actual command contend
            indexOfLinebreak = rawStr.find(b"\r")+1
            rawSubStr = bytearray()

            end = rawStr.find(b"\r", indexOfLinebreak)
            rawSubStr = rawStr[indexOfLinebreak+1:end]
            return rawSubStr.decode("utf-8")

        case 42: #*
            #*<number-of-elements>\r\n<element-1>...<element-n> |||| *3\r\n$3\r\nSET\r\n$5\r\nmykey\r\n$5\r\nvalue\r\n*2\r\n$3\r\nGET\r\n$5\r\nmykey\r\n
            pos = 0
            n = len(rawStr)
            out = []

            if rawStr[pos] != ord('*'):
                raise ValueError("Expected array start '*'")
            
            pos += 1
            end = rawStr.find(b'\r\n', pos)
            n_elements = int(rawStr[pos:end])
            pos = end + 2

            for _ in range(n_elements):
                prefix = rawStr[pos]
                pos += 1

                if prefix == ord('$'):  # bulk string
                    end = rawStr.find(b'\r\n', pos)
                    length = int(rawStr[pos:end])
                    pos = end + 2
                    arg = rawStr[pos:pos+length].decode("utf-8")
                    pos += length + 2  # skip trailing \r\n
                    out.append(arg)

                elif prefix == ord('+'):  # simple string
                    end = rawStr.find(b'\r\n', pos)
                    out.append(rawStr[pos:end].decode("utf-8"))
                    pos = end + 2

                elif prefix == ord('-'):  # error
                    end = rawStr.find(b'\r\n', pos)
                    out.append(rawStr[pos:end].decode("utf-8"))  # or raise
                    pos = end + 2

                elif prefix == ord(':'):  # integer
                    end = rawStr.find(b'\r\n', pos)
                    out.append(int(rawStr[pos:end]))
                    pos = end + 2

                else:
                    raise ValueError(f"Unsupported prefix: {chr(prefix)}")

            return out
        case "#":
            return "Boolean (RESP3)"

        # Default case
        case _:
            return f"Unknown prefix: {prefix}"