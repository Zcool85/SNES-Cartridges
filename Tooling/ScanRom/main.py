import struct
import sys

# https://snes.nesdev.org/wiki/ROM_file_formats

def is_headered(rom_data):
    """
    the headered version has 512 extra bytes at the start of the file.
    Because ROM files are generally expected to include complete 32 or 64 kb banks, a simple way
    of detecting a header is by checking if the file size modulo 1024 is equal to 512.
    
    Args:
        rom_data (bytes): Contenu binaire de la ROM.
        
    Returns:
        bool: True si la ROM a un en-tête, False sinon.
    """

    print(f"Check header - file size : {len(rom_data)}")
    print(f"Check header - modulo 1024 : {len(rom_data) % 1024}")
    
    return len(rom_data) % 1024 == 512

def analyze_snes_rom(rom_path):
    with open(rom_path, "rb") as f:
        rom_data = f.read()

    if is_headered(rom_data):
        print(f"ROM avec header !")
    else:
        print(f"Pas de header")

    # ROM Header located at :
    # - $007FC0-$007FDF : For LoROM
    # - $00FFC0-$00FFDF : For HiROM
    # - $40FFC0-$40FFDF : For ExHiROM

    game_title = struct.unpack("<21s", rom_data[0x00FFC0:0x00FFD5])
    print(f"game_title = {game_title}")
    map_mode = struct.unpack("<B", rom_data[0x00FFD5:0x00FFD6])[0]

    if map_mode & 0xE0 != 0x20:
        print("NOT GOOD HEADER !!!")
    
    if map_mode & 0x10 == 0:
        print("Slow speed (200ns)")
    else:
        print("Fast speed (120ns)")

    match map_mode & 0x0F:
        case 0:
            print("MAP LoROM (Mode 20)")
            print("   LoROM is mapped to $808000-$FFFFFF in 32K blocks,")
            print("   skipping a15 and a23. Most is mirrored down to $008000.")
        case 1:
            print("MAP HiROM (Mode 21)")
            print("   HiROM is mapped to $C00000-$FFFFFF linearly.")
            print("   It is mirrored down to $400000, and the second half of")
            print("   each 64K bank is mirrored to $008000 and $808000.")
            print("   C00000-FFFFFF skipping a22, a23")
        case 5:
            print("MAP ExHiROM (Mode 25)")
            print("   ExHiROM is mapped to $C00000-$FFFFFF followed by")
            print("   $400000-$7FFFFF.  There are two inaccessible 32K holes")
            print("   near the end, and two 32K blocks that are accessible only")
            print("   through their mirrors to $3E8000 and $3F8000.")
            print("   skipping a22, inverting a23")
        case _:
            print("Unkwnown map")

    cartridge_type = struct.unpack("<B", rom_data[0x00FFD6:0x00FFD7])[0]
    
    match cartridge_type:
        case 0x00:
            print("ROM only")
        case 0x01:
            print("ROM + RAM")
        case 0x02:
            print("ROM + RAM + battery")
        case 0x03:
            print("ROM + coprocessor DSP")
        case 0x04:
            print("ROM + coprocessor DSP + RAM")
        case 0x05:
            print("ROM + coprocessor DSP + RAM + battery")
        case 0x06:
            print("ROM + coprocessor DSP + battery")

        case 0x13:
            print("ROM + coprocessor GSU (Super FX)")
        case 0x14:
            print("ROM + coprocessor GSU (Super FX) + RAM")
        case 0x15:
            print("ROM + coprocessor GSU (Super FX) + RAM + battery")
        case 0x16:
            print("ROM + coprocessor GSU (Super FX) + battery")

        case 0x23:
            print("ROM + coprocessor OBC1")
        case 0x24:
            print("ROM + coprocessor OBC1 + RAM")
        case 0x25:
            print("ROM + coprocessor OBC1 + RAM + battery")
        case 0x26:
            print("ROM + coprocessor OBC1 + battery")

        case 0x33:
            print("ROM + coprocessor SA-1")
        case 0x34:
            print("ROM + coprocessor SA-1 + RAM")
        case 0x35:
            print("ROM + coprocessor SA-1 + RAM + battery")
        case 0x36:
            print("ROM + coprocessor SA-1 + battery")

        case 0x43:
            print("ROM + coprocessor S-DD1")
        case 0x44:
            print("ROM + coprocessor S-DD1 + RAM")
        case 0x45:
            print("ROM + coprocessor S-DD1 + RAM + battery")
        case 0x46:
            print("ROM + coprocessor S-DD1 + battery")

        case 0x53:
            print("ROM + coprocessor S-RTC")
        case 0x54:
            print("ROM + coprocessor S-RTC + RAM")
        case 0x55:
            print("ROM + coprocessor S-RTC + RAM + battery")
        case 0x56:
            print("ROM + coprocessor S-RTC + battery")

        case 0xE3:
            print("ROM + coprocessor Other (Super Game Boy/Satellaview)")
        case 0xE4:
            print("ROM + coprocessor Other (Super Game Boy/Satellaview) + RAM")
        case 0xE5:
            print("ROM + coprocessor Other (Super Game Boy/Satellaview) + RAM + battery")
        case 0xE6:
            print("ROM + coprocessor Other (Super Game Boy/Satellaview) + battery")

        case 0xF3:
            print("ROM + coprocessor Custom (specified with $FFBF)")
        case 0xF4:
            print("ROM + coprocessor Custom (specified with $FFBF) + RAM")
        case 0xF5:
            print("ROM + coprocessor Custom (specified with $FFBF) + RAM + battery")
        case 0xF6:
            print("ROM + coprocessor Custom (specified with $FFBF) + battery")

    rom_size = struct.unpack("<B", rom_data[0x00FFD7:0x00FFD8])[0]
    print(f"ROM Size : {1 << rom_size} KB")

    ram_size = struct.unpack("<B", rom_data[0x00FFD8:0x00FFD9])[0]
    print(f"RAM Size : {1 << ram_size} KB")

    destination_code = struct.unpack("<B", rom_data[0x00FFD9:0x00FFDA])[0]
    match destination_code:
        case 0x00:
            print("Country : J - Japan (NTSC)")
        case 0x01:
            print("Country : E - North America - USA and Canada (NTSC)")
        case 0x02:
            print("Country : P - Aurope, Oceania, Asia (PAL)")
        case 0x03:
            print("Country : W - Scandinavia (PAL)")
        case 0x04:
            print("Country : - - Finland (PAL)")
        case 0x05:
            print("Country : - - Denmark (PAL)")
        case 0x06:
            print("Country : F - Europe - French only (PAL)")
        case 0x07:
            print("Country : H - Holland (PAL)")
        case 0x08:
            print("Country : S - Spanish (PAL)")
        case 0x09:
            print("Country : D - German (PAL)")
        case 0x0A:
            print("Country : I - Italy (PAL)")
        case 0x0B:
            print("Country : C - China (PAL)")
        case 0x0C:
            print("Country : - - Indonesia (PAL)")
        case 0x0D:
            print("Country : K - South Korea (NTSC)")
        case 0x0E:
            print("Country : A - Common (???)")
        case 0x0F:
            print("Country : N - Canada (NTSC)")
        case 0x10:
            print("Country : B - Brazil (NTSC)")
        case 0x11:
            print("Country : U - Australia (PAL)")
        case 0x12:
            print("Country : X - Other Variation (???)")
        case 0x13:
            print("Country : Y - Other Variation (???)")
        case 0x14:
            print("Country : Z - Other Variation (???)")
        case _:
            print("Country unknown")

    developper_id = struct.unpack("<B", rom_data[0x00FFDA:0x00FFDB])[0]
    print(f"developper_id : {developper_id}")
    # TODO : If = 0x33, go too expended cartridge header

    rom_version = struct.unpack("<B", rom_data[0x00FFDB:0x00FFDC])[0]
    print(f"rom_version : {rom_version}")

    # TODO : Checksums
    # TODO : Add Expended cartridge header
    # TODO : Get header for LoROM and ExHiROM
    # TODO : Add header verification


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <rom_path>")
        sys.exit(1)

    rom_path = sys.argv[1]
    analyze_snes_rom(rom_path)
