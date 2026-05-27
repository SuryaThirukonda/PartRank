
import json


with open("gpu_data.json", "r") as j:
    data = json.load(j)
    bad = ["Intel HD", "intel uhd", "integrated", "m", "firepro", "max-q", "mobile", "laptop"]
    bad.extend(["tesla", "a100", "v100", "p100", "k80", "titan", "quadro"])
    bad.extend(["Quadro","RTX PRO","RTX A","Ada Generation","Radeon PRO W","Radeon Pro W","Radeon Pro WX","Radeon Pro V","Radeon Instinct","FirePro"])
    bad.extend(["GRID", "MxGPU"])
    bad.append("GRE")
    bad.append("nvidia l")
    bad.append("nvidia a")
    bad.append("p1")
    bad.extend(["Ryzen","Snapdragon","Qualcomm Adreno","Intel Iris Xe","Intel Iris Pro", "Intel Iris Plus","Intel UHD","Intel HD","Radeon Vega","Vega M","610M","780M","760M","740M","890M","880M","860M","840M","820M"])
    bad.extend(["USB Display","Miracast","spacedesk","Mirror Driver","DameWare","VMware","Indirect Display","IddCX","IDDCX","Display Device","Display Driver","Matrox","Barco","EIZO","EPSON","OrayIdd","SQExtFrame","LuminonCore","extension Adapter","Custom GPU","ICE DISPLAY","B8DKMDAP","Embedded GPU"])
    bad.extend(["Embedded", "Moore Threads", "TURZX", "Citrix", "TENSOR", "FireStream", "RadeonT"])
    bad.extend([
  # Laptop / Mobile
  "Laptop GPU",
  "(Mobile)",
  "Max-Q",

  # Datacenter / Tesla / Compute
  "Tesla",
  "A100",
  "NVIDIA A10",
  "NVIDIA A40",
  "NVIDIA L",
  "nVidia L",
  "L40S",
  "L40-",
  "L20-",
  "L4-",
  " L2 ",
  "A16",
  "A10G",

  # vGPU slices (bare suffix patterns)
  "-48Q", "-24Q", "-16Q", "-12Q", "-8Q", "-6Q", "-4Q", "-3Q", "-2Q", "-1Q",
  "-16A", "-12A", "-8A", "-6A", "-4A", "-3A", "-2A", "-1A",
  "-16B", "-12B", "-8B", "-6B", "-4B", "-3B", "-2B", "-1B",
  "RTXA",
  "GRID",
  "MxGPU",

  # Workstation / Professional
  "Quadro",
  "RTX PRO",
  "RTX A",
  "Ada Generation",
  "Radeon PRO W",
  "Radeon Pro W",
  "Radeon Pro WX",
  "Radeon Pro V",
  "Radeon Instinct",
  "FirePro",

  # iGPU / APU
  "Ryzen",
  "EPYC",
  "Snapdragon",
  "Qualcomm Adreno",
  "Intel Iris Xe",
  "Intel Iris Pro",
  "Intel Iris Plus",
  "Intel Iris ",
  "Intel UHD",
  "Intel HD",
  "Intel Coffee Lake",
  "Intel Graphics",
  "Radeon Vega 3",
  "Radeon Vega 6",
  "Radeon Vega 8",
  "Radeon Vega 9",
  "Radeon Vega 10",
  "Radeon Vega 11",
  "Radeon RX Vega 6",
  "Radeon RX Vega 8",
  "Radeon RX Vega 10",
  "Radeon RX Vega 11",
  "Radeon RX Vega11",
  "Athlon Gold",
  "Vega M",
  "890M", "880M", "860M", "840M", "820M",
  "780M", "760M", "740M",

  # APU Dual-graphics combos
  " Dual",
  "7660D +",
  "7560D +",
  "8670D +",
  "8570D +",

  # Mining cards
  "P102-",
  "P104-",
  "P106-",

  # GRE (China-only)
  "GRE",

  # Junk / virtual / fake drivers
  "USB Display",
  "Miracast",
  "spacedesk",
  "Mirror Driver",
  "DameWare",
  "VMware",
  "VirtIO",
  "Indirect Display",
  "IddCX",
  "IDDCX",
  "Display Device",
  "Display Driver",
  "Matrox",
  "Barco",
  "EIZO",
  "EPSON",
  "OrayIdd",
  "SQExtFrame",
  "LuminonCore",
  "extension Adapter",
  "Custom GPU",
  "ICE DISPLAY",
  "B8DKMDAP",
  "Winsta0",
  "GDIHOOK",
  "Red Hat VirtIO",
  "N18E-Q1",
  "N16P-GX",
  "Q12U-1",
  "OPAL XT",
  "Glenfly",
  "NVS ",
  "GeForce GPU",
  "Radeon Sky 500",
  "Radeon E9550",
  "Radeon E8870",
  "Radeon E8860",
  "Embedded GPU",
  "Moore Threads",
  "TURZX",
  "Citrix",
  "TENSOR",
  "FireStream",
  "RadeonT",
  "Radeon TM",
  "Radeon EPYC",
  "Inspiration CG",
  "Radeon AI PRO",
  "Radeon Pro SSG",

  # OEM-only low-end GeForce A-suffix
  "960A", "950A", "945A", "940A", "930A", "840A", "830A", "745A", "760A",

  # Misc
  "PCI GDIHOOK",
  "LIANLI USB",
  "SMI USB",
  "AicUsbDisplay",
  "Racer-Tech",
  "Fresco Logic"
])
    filtered_data = [gpu for gpu in data if not any(bad_word.lower() in gpu["name"].lower() for bad_word in bad)]
    with open("gpu_data_cleaned_2.json", "w") as j:
        json.dump(filtered_data, j, indent=4)