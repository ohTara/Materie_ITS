import os
import random
import zlib
import gzip
import bz2
import lzma
import math
from collections import Counter
import time

def calculate_entropy(data):
    """Calcola l'entropia di Shannon di una sequenza di dati"""
    if not data:
        return 0
    
    # Conta la frequenza di ogni byte
    counter = Counter(data)
    length = len(data)
    
    # Calcola l'entropia
    entropy = 0
    for count in counter.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    
    return entropy

def theoretical_min_size(entropy, data_size):
    """Calcola la dimensione minima teorica in base all'entropia"""
    return (entropy * data_size) / 8  # in bytes

def create_files():
    """Crea i due file di test da 1MB ciascuno"""
    print("🔧 Creazione dei file di test...")
    
    # File 1: Solo lettere 'a' (1MB)
    file1_name = "file_solo_a.txt"
    with open(file1_name, 'w', encoding='utf-8') as f:
        # 1MB = 1,048,576 bytes
        f.write('a' * 1048576)
    
    # File 2: Caratteri ASCII casuali (1MB)
    file2_name = "file_ascii_random.txt"
    with open(file2_name, 'w', encoding='utf-8') as f:
        # Genera caratteri ASCII casuali (32-126)
        random_chars = ''.join(chr(random.randint(32, 126)) for _ in range(1048576))
        f.write(random_chars)
    
    print(f"✅ Creati {file1_name} e {file2_name}")
    return file1_name, file2_name

def compress_file(filename, method='gzip'):
    """Comprime un file usando l'algoritmo specificato"""
    with open(filename, 'rb') as f:
        data = f.read()
    
    if method == 'gzip':
        compressed = gzip.compress(data, compresslevel=9)
        suffix = '.gz'
    elif method == 'bz2':
        compressed = bz2.compress(data, compresslevel=9)
        suffix = '.bz2'
    elif method == 'lzma':
        compressed = lzma.compress(data, preset=9)
        suffix = '.xz'
    elif method == 'zlib':
        compressed = zlib.compress(data, level=9)
        suffix = '.zlib'
    
    compressed_filename = f"{filename}_{method}{suffix}"
    with open(compressed_filename, 'wb') as f:
        f.write(compressed)
    
    return compressed_filename, len(compressed)

def analyze_file(filename):
    """Analizza un file calcolando entropia e statistiche"""
    with open(filename, 'rb') as f:
        data = f.read()
    
    size = len(data)
    entropy = calculate_entropy(data)
    min_theoretical_size = theoretical_min_size(entropy, size)
    
    # Conta caratteri unici
    unique_chars = len(set(data))
    
    return {
        'size': size,
        'entropy': entropy,
        'min_theoretical_size': min_theoretical_size,
        'unique_chars': unique_chars,
        'data': data
    }

def print_separator():
    print("=" * 80)

def print_header(title):
    print(f"\n{'=' * 20} {title} {'=' * 20}")

def main():
    print("🎯 ANALISI PRATICA DI ENTROPIA E COMPRESSIONE")
    print("Questo script dimostra empiricamente i limiti teorici della compressione")
    print_separator()
    
    # Crea i file
    file1, file2 = create_files()
    
    # Analizza i file originali
    print_header("ANALISI DEI FILE ORIGINALI")
    
    print("\n📊 FILE 1 - Solo lettere 'a':")
    analysis1 = analyze_file(file1)
    print(f"   Dimensione: {analysis1['size']:,} bytes (1MB)")
    print(f"   Entropia: {analysis1['entropy']:.6f} bit per simbolo")
    print(f"   Caratteri unici: {analysis1['unique_chars']}")
    print(f"   Dimensione minima teorica: {analysis1['min_theoretical_size']:.2f} bytes")
    print(f"   💡 Spiegazione: Un file con solo 'a' ha entropia quasi 0!")
    print(f"      Questo significa che contiene pochissima informazione reale.")
    
    print("\n📊 FILE 2 - ASCII casuali:")
    analysis2 = analyze_file(file2)
    print(f"   Dimensione: {analysis2['size']:,} bytes (1MB)")
    print(f"   Entropia: {analysis2['entropy']:.6f} bit per simbolo")
    print(f"   Caratteri unici: {analysis2['unique_chars']}")
    print(f"   Dimensione minima teorica: {analysis2['min_theoretical_size']:.2f} bytes")
    print(f"   💡 Spiegazione: Caratteri casuali hanno alta entropia!")
    print(f"      Contengono molta informazione e sono difficili da comprimere.")
    
    # Compressione
    print_header("COMPRESSIONE CON DIVERSI ALGORITMI")
    
    algorithms = ['gzip', 'bz2', 'lzma', 'zlib']
    
    for file_name, analysis, file_desc in [(file1, analysis1, "Solo 'a'"), 
                                          (file2, analysis2, "ASCII casuali")]:
        print(f"\n🗜️  COMPRESSIONE: {file_desc}")
        print(f"   File originale: {file_name}")
        
        for algo in algorithms:
            start_time = time.time()
            compressed_file, compressed_size = compress_file(file_name, algo)
            compress_time = time.time() - start_time
            
            compression_ratio = analysis['size'] / compressed_size
            space_saved = analysis['size'] - compressed_size
            percentage_saved = (space_saved / analysis['size']) * 100
            
            print(f"\n   📁 {algo.upper()}:")
            print(f"      File compresso: {compressed_file}")
            print(f"      Dimensione: {compressed_size:,} bytes")
            print(f"      Rapporto compressione: {compression_ratio:.2f}:1")
            print(f"      Spazio risparmiato: {space_saved:,} bytes ({percentage_saved:.1f}%)")
            print(f"      Tempo compressione: {compress_time:.3f} secondi")
            
            # Confronto con il limite teorico
            if analysis['min_theoretical_size'] > 0:
                efficiency = analysis['min_theoretical_size'] / compressed_size * 100
                print(f"      Efficienza vs limite teorico: {efficiency:.1f}%")
    
    # Analisi teorica finale
    print_header("ANALISI TEORICA E CONCLUSIONI")
    
    print("\n🧠 TEORIA DELL'INFORMAZIONE:")
    print("   • L'ENTROPIA misura la quantità di informazione in un messaggio")
    print("   • Più alta è l'entropia, più informazione c'è da rappresentare")
    print("   • Il LIMITE DI SHANNON stabilisce il limite teorico di compressione")
    print("   • Nessun algoritmo può comprimere oltre questo limite senza perdere informazione")
    
    print(f"\n📈 RISULTATI EMPIRICI:")
    print(f"   • File con solo 'a': Entropia ≈ {analysis1['entropy']:.4f} bit/simbolo")
    print(f"     → Comprimibile quasi al 100% (pochissima informazione reale)")
    print(f"   • File casuale: Entropia ≈ {analysis2['entropy']:.4f} bit/simbolo")
    print(f"     → Difficile da comprimere (molta informazione reale)")
    
    print(f"\n🎯 CONCLUSIONI PRATICHE:")
    print(f"   • Dati ripetitivi (bassa entropia) = alta compressibilità")
    print(f"   • Dati casuali (alta entropia) = bassa compressibilità")
    print(f"   • Gli algoritmi di compressione cercano pattern per ridurre la ridondanza")
    print(f"   • Il limite teorico di Shannon è raramente raggiunto in pratica")
    
    print(f"\n🔍 APPLICAZIONI REALI:")
    print(f"   • File di testo: Spesso comprimibili (linguaggio ha pattern)")
    print(f"   • Immagini JPEG: Già compresse, difficili da comprimere ulteriormente")
    print(f"   • File eseguibili: Moderatamente comprimibili")
    print(f"   • Dati crittografati: Quasi incomprimibili (sembrano casuali)")
    
    print_separator()
    print("✅ ANALISI COMPLETATA!")
    print("I file compressi sono stati salvati nella directory corrente.")
    
    # Pulizia opzionale
    print(f"\n🧹 Per pulire i file generati, esegui:")
    print(f"   rm file_solo_a.txt* file_ascii_random.txt*")

if __name__ == "__main__":
    main()
