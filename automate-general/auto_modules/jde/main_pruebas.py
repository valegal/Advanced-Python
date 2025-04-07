
from review import review_pdfs
import time

def main():
    

    batchcarga = {
    '1': '29804',
    '3': '29806',
    '4': '29807'
    }

    valores_columna_dos = review_pdfs(batchcarga)
    print(valores_columna_dos) 

    # navigate_home(driver)
    time.sleep(5)

    print("Vamos muy bien!")



if __name__ == "__main__":
    main()
