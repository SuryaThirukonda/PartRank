import json

# Substring filters — safe broad terms
bad_substrings = [
    "Intel HD", "Intel UHD", "integrated", "firepro", "max-q", "mobile", "laptop",
    "tesla", "a100", "v100", "p100", "k80", "titan", "quadro",
    "Quadro", "RTX PRO", "Ada Generation",
    "Radeon PRO W", "Radeon Pro W", "Radeon Pro WX", "Radeon Pro V",
    "Radeon Instinct", "FirePro", "GRID", "MxGPU", "GRE",
    "nvidia l", "nvidia a",
    "Ryzen", "Snapdragon", "Qualcomm Adreno",
    "Intel Iris Xe", "Intel Iris Pro", "Intel Iris Plus", "Intel Iris ",
    "Intel Coffee Lake", "Intel Graphics",
    "Radeon Vega", "Vega M",
    "610M", "780M", "760M", "740M", "890M", "880M", "860M", "840M", "820M",
    "USB Display", "Miracast", "spacedesk", "Mirror Driver", "DameWare",
    "VMware", "VirtIO", "Indirect Display", "IddCX", "IDDCX",
    "Display Device", "Display Driver", "Matrox", "Barco", "EIZO", "EPSON",
    "OrayIdd", "SQExtFrame", "LuminonCore", "extension Adapter",
    "Custom GPU", "ICE DISPLAY", "B8DKMDAP", "Winsta0", "GDIHOOK",
    "Red Hat VirtIO", "N18E-Q1", "N16P-GX", "OPAL XT",
    "NVS ", "GeForce GPU", "Embedded GPU", "Embedded",
    "Moore Threads", "TURZX", "Citrix", "TENSOR", "FireStream",
    "RadeonT", "Radeon TM", "Radeon EPYC", "Inspiration CG",
    "Radeon AI PRO", "Glenfly", "PCI GDIHOOK", "LIANLI USB",
    "SMI USB", "AicUsbDisplay", "Racer-Tech", "Fresco Logic",
    # APU dual-graphics combos — every combo entry contains " + "
    " + ",
    # vGPU slice suffixes
    "P102-", "P104-", "P106-",
    "-48Q", "-24Q", "-16Q", "-12Q", "-8Q", "-6Q", "-4Q", "-3Q", "-2Q", "-1Q",
    "-16A", "-12A", "-8A", "-6A", "-4A", "-3A", "-2A", "-1A",
    "-16B", "-12B", "-8B", "-6B", "-4B", "-3B", "-2B", "-1B",
    "RTXA", "-serie", "Seria ",
    "Opteron", "FX-9", "R7 A8-", "R7 A10-", "R7 A12-", "R5 A6-",
    "8060S", "8050S", "8040S",
    "6800S", "7600S", "7700S", "6600S",
    "Intel Arc Pro", "Arc B390", "Arc B370",
    "Arc 140T", "Arc 130T", "Arc 140V", "Arc 130V",
    "Arc A380E", "Arc A310 LP",
    # APU iGPU
    "Radeon RX Vega", "Radeon RX Vega11",
    "Radeon EPYC", "Athlon Gold",
    "Intel Iris",
    # OEM A-suffix GeForce
    "960A", "950A", "945A", "940A", "930A", "840A", "830A", "745A", "760A",
    # Embedded Radeon
    "Radeon E8870", "Radeon E8860", "Radeon E9550", "Radeon Sky 500",
    # Dual combos using slash format
    "7660D +", "7560D +", "8670D +", "8570D +",
    # Misc
    "Q12U-1", "N18E-Q1", "N16P-GX",
    # Add these to bad_substrings:
    "M XT",       # catches 6850M XT etc.
    "MX",         # catches all GeForce MX series
    "M | ",       # catches mobile entries where M is at end of name
    " 680M",      # specific mobile
    "Mobility",
    "CMP ",       # mining
    "Eng Sample",
    "OEM",
    "RTX A",      # workstation RTX A-series — add back now that RTX A4070 etc don't exist
    "MS Idd",
    "Mirage Driver",
    "MIRRORV3",
    "Sharing Monitor",
    "MONSTER GeForce",  # modded GPU name
    "- MODDED",
    "GME",        # China OEM RX 590
    " M | ",
    "Radeon R9 M",
    "Radeon R7 M",
    "Radeon HD 8", # catches 8870M, 8790M, 8750M, 8690M, 8600/8700M
    "HD 7970M", "HD 7850M", "HD 7750M", "HD 7690M", "HD 7870M",
    "HD 6900M", "HD 6970M", "HD 6700M",
    "Arc A770M", "Arc A730M", "Arc A530M", "Arc A370M",
    "Radeon Pro 5600M", "Radeon Pro 5500M", "Radeon Pro 5300M",
    "GTX 980M", "GTX 970M", "GTX 965M", "GTX 960M", "GTX 870M",
    "GTX 850M", "GTX 775M", "GTX 770M", "GTX 765M", "GTX 750M",
    "GTX 745M", "GTX 680M", "GTX 675M", "GTX 670M", "GTX 660M",
    "GTX 580M", "GTX 570M", "GTX 560M", "GTX 485M", "GTX 480M",
    "GTX 470M", "GTX 460M", "GT 755M", "GT 750M", "GT 745M", "GT 650M",
    "945M", "940MX", "940M", "930MX", "930M", "920MX", "845M", "830M",
    "770M", "680MX",
    "Radeon 680M", "Radeon 660M"
]


# Exact name matches — too short or generic to use as substrings
bad_exact = {
    # China-only D variants
    "GeForce RTX 5090 D", "GeForce RTX 5090 D v2", "GeForce RTX 4090 D",
    # Datacenter bare names
    "L4", "L2", "L40S", "A16",
    # NVIDIA T-series workstation
    "NVIDIA T1000 8GB", "NVIDIA T1000", "NVIDIA T600", "NVIDIA T500",
    "T400 4GB", "T400",
    # vGPU bare names
    "RTX6000-Ada-6Q", "RTX6000-Ada-3A", "RTX5000-Ada-4Q",
    "A10-24Q", "A10-12Q", "A10-8Q", "A10-4Q", "A10G",
    "A40-48Q", "A40-8Q", "A40-3Q", "A40-12Q", "A40-6Q",
    "A40-24Q", "A40-4Q", "A40-2Q",
    "A16-8Q", "A16-2Q", "A16-16Q", "A16-4Q", "A16-1Q",
    "A16-1B", "A16-2B", "A16-16A",
    "A2-4Q", "A2-2Q", "Q12U-1",
    # Intel Arc generic
    "Intel Arc GPU", "Intel Arc",
    # Radeon Pro workstation / Mac-internal
    "Radeon Pro 5700 XT", "Radeon Pro 5700", "Radeon Pro 5500 XT",
    "Radeon Pro 5300", "Radeon Pro 580X", "Radeon Pro 580", "Radeon Pro 570",
    "Radeon Pro 560X", "Radeon Pro 560", "Radeon Pro 465", "Radeon Pro 460",
    "Radeon Pro 455", "Radeon Pro 450", "Radeon Pro 555", "Radeon Pro Duo",
    "Radeon Pro SSG", "Radeon Pro",
    # OEM / China-only
    "Radeon RX 5700 XT 50th Anniversary", "GeForce RTX 2060 12GB",
    "GeForce RTX 3060 8GB", "GeForce RTX 2050", "GeForce GTX 1060 5GB",
    "Radeon RX 6600 LE", "Radeon RX 6500", "Radeon RX 5600", "Radeon RX 5300",
    "Radeon RX 7400", "Radeon RX 580 2048SP", "Radeon RX 580X",
    "Radeon RX 560X", "Radeon RX 550X", "Radeon RX 540", "Radeon RX 640",
    "Radeon RX 570X", "Radeon RX 6300",
    # Non-existent scrape artifacts
    "Radeon RX 670", "Radeon RX 780", "Radeon RX 7500",
    # Budget OEM / iGPU-tier
    "Radeon 625", "Radeon 630", "Radeon 530", "Radeon 535",
    "Radeon 540", "Radeon 540X", "Radeon 550X", "Radeon 550",
    # OEM-only old hardware
    "Radeon HD 8990", "Radeon HD 8950", "Radeon HD 8770",
    "Radeon HD 6850 X2", "Radeon HD 4870 X2", "Radeon HD 4850 X2",
    "GeForce GT 645", "GeForce GTX 645", "GeForce GTX 555",
    "GeForce GTX 650 Ti BOOST",
    # Localized artifacts
    "Radeon HD 7800-serie", "Radeon HD 7700-serie", "Seria Radeon HD 7700",
    # APU iGPU exact names
    "Radeon RX Vega 11 PRD", "Radeon RX Vega 11 Processor",
    "Radeon RX Vega 10", "Radeon RX Vega11", "Radeon RX Vega 8", "Radeon RX Vega 6",
    "Radeon RX Vega 11",
    "Radeon Athlon Gold PRO 4150GE",
    "Intel Iris P555", "Intel Iris 550", "Intel Iris 540", "Intel Iris 650",
    "Intel Coffee Lake UHD", "Intel Graphics",
    # Junk / driver entries
    "Winsta0\\Default", "PCI GDIHOOK5", "Red Hat VirtIO GPU DOD controller",
    "OPAL XT/GL", "Glenfly Arise-GT-10C0", "NVS 810", "GeForce GPU",
    "N18E-Q1", "N16P-GX",
    # Misc
    "Radeon E9550", "Radeon E8870PCIe", "Radeon E8860", "Radeon Sky 500",
    "Radeon AI PRO R9700", "Radeon HD 7670A",
    # OEM A-suffix GeForce
    "GeForce GTX 960A", "GeForce GTX 950A", "GeForce GT 745A",
    "GeForce GTX 760A", "GeForce 945A", "GeForce 940A",
    "GeForce 930A", "GeForce 840A", "GeForce 830A",
}

with open("gpu_data.json", "r") as j:
    data = json.load(j)

filtered_data = []
excluded = []

for gpu in data:
    name = gpu["name"]
    # Exact match check first (fast set lookup)
    if name in bad_exact:
        excluded.append((name, "exact match"))
        continue
    # Substring check
    if any(s.lower() in name.lower() for s in bad_substrings):
        excluded.append((name, "substring match"))
        continue
    filtered_data.append(gpu)

with open("gpu_data_cleaned_4.json", "w") as j:
    json.dump(filtered_data, j, indent=4)

with open("gpu_data_cleaned_4.json", "r") as j:
    gpus = json.load(j)
    print(len(gpus))

with open("gpu_data_cleaned_3.json", "r") as j:
    gpus = json.load(j)
    print(len(gpus))

with open("gpu_data.json", "r") as j:
    gpus = json.load(j)
    print(len(gpus))

