# SNES Cartridge

Try to reproduce SNES Cartridge with different variants, but with actual ROM chips.

My goal is to produce a home made cartridge for this to games in the first time :
- Final Fantasy VI with FR traductions - "Final Fantasy VI (Traduit en Français) (v3.1).smc" (HiROM + 8KB SRAM + 4MB + Batt)
- Hyper Metroid

We cannot make games that require SuperFX, SuperFX2, DSP chips, SA-1, C4, S-DD1, or SPC7110 chips.


## Documentation

Cf. [Mouse Bite Lab](https://mousebitelabs.com/2019/05/18/custom-pcb-explanation/).


## Recents EEPROM

I choose to use EEPROM relatively recent with parallel interface.

EEPROM because I want to reuse chips wen possible and I can make mistakes without drop the chip.

Now, with this constraint, a can use one oof the following EEPROM : (Non-exhaustive list)

| Size (Mbits) | Size (Mbytes) | Voltage | Read Acces Time | Device       | Price    |
|-------------:|--------------:|--------:|----------------:|:-------------|---------:|
| 8 Mb         | 1 MB          | 3v      | 55 ns           | S29AL008J    | ~1.79 €  |
| 16 Mb        | 2 MB          | 3v      | 70 ns           | SST39VF1601C | ~2.77 €  |
| 16 Mb        | 2 MB          | 3v      | 55 ns           | S29AL016J    | ~3.12 €  |
| 32 Mb        | 4 MB          | 3v      | 70 ns           | SST39VF3201C | ~3.43 €  |
| 32 Mb        | 4 MB          | 3v      | 70 ns           | S29JL032J    | ~3.27 €  |
| 64 Mb        | 8 MB          | 3v      | 90 ns           | SST38VF6401  | ~7.58 €  |
| 64 Mb        | 8 MB          | 3v      | 70 ns           | S29GL064S    | ~3.57 €  |
| 128 Mb       | 16 MB         | 3v      | 90 ns           | S29GL128S    | ~4.58 €  |
| 256 Mb       | 32 MB         | 3v      | 90 ns           | S29GL256S    | ?        |
| 512 Mb       | 64 MB         | 3v      | 100 ns          | S29GL512S    | ~8.18 €  |
| 1 Gb         | 128 MB        | 3v      | 100 ns          | S29GL01GS    | ?        |

The maximum alocatable adresse space is 00:0000 to FF:FFFFF corresponding to 128Mb (16MB) ROM size (only for unique game in cartridge and without mapping).

Voltage adapter 8 bits : 74LVC245 (Exemple SN74LVCC3245A) - Around 10ns of time response (~1.2 €)


## SRAM replacement

Starndard : AS6C6264 (Warn : 3.3v typique, but OK with 5V)



I choose F-RAM to replace SRAM. I don't need Batterie with F-RAM.

Exemples :
- FM16W08 (64Kb / 8KB)
- FM18W08 (256Kb / 32KB)


## In progress...

[Memory MAP](https://m.youtube.com/watch?v=PvfhANgLrm4&list=PLHQ0utQyFw5KCcj1ljIhExH_lvGwfn6GV&index=13&pp=iAQB)
[SNES Memory MAP](https://mousebitelabs.com/2019/05/18/custom-pcb-explanation/#sram).
[SNES Memory MAP](https://en.wikibooks.org/wiki/Super_NES_Programming/SNES_memory_map).
[SNES Hardware specs](https://problemkaputt.de/fullsnes.htm#snescarthirommappingromdividedinto64kbanksaround500games).
[SNES Memory MAP](https://snes.nesdev.org/wiki/Memory_map).

[ROM File format](https://snes.nesdev.org/wiki/ROM_file_formats).

[SNES ROM Header](https://snes.nesdev.org/wiki/ROM_header).
[Cartridge Header](https://emudev.de/q00-snes/cartridge-header/).

