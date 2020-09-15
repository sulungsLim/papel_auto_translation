from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import time
import requests
import pandas as pd


class translation:

    def __init__(self,path):
        '''
        path : 경로 넣어주자

        '''
        print("코로나 조심해")
        name = path.split("/")[-2]
        paper = self.read_pdf_PDFMINER(path)
        paper = paper.replace("\n","")
        paper = paper.replace("-", "")
        paper_list = paper.split(".")
        eng_list = []
        kor_list = []
        double_list = []
        for sentence in paper_list:
            try:
                eng = sentence
                kor = self.kor2eng(sentence)
                eng_list.append(eng)
                kor_list.append(kor)
                double_list.append(eng)
                double_list.append(kor)
                print(eng)
                print(kor)
                if len(eng_list)%20 == 0:
                    time.sleep(1)
            except:
                pass

        eng_df = pd.DataFrame(eng_list)
        kor_df = pd.DataFrame(kor_list)
        db_df = pd.DataFrame(double_list)
        df_axis1 = pd.concat([eng_df, kor_df], axis=1)  # column bind
        db_df.to_csv('%s_번역한줄씩.txt'%(name),index=False, header=None)
        df_axis1.to_csv('%s_번역병렬.txt'%(name) ,index=False, header=None)

        print(df_axis1)
        print(db_df)




    def kor2eng(self,query):
        '''
        카카오 번역 스크래핑
        qurey : 문장 넣어주자
        '''
        url = "https://translate.kakao.com/translator/translate.json"

        headers = {
            "Referer": "https://translate.kakao.com/",
            "User-Agent": "Mozilla/5.0"
        }

        data = {
            "queryLanguage": "en",
            "resultLanguage": "kr",
            "q": query
        }

        resp = requests.post(url, headers=headers, data=data)
        data = resp.json()

        output = data['result']['output'][0][0]
        return output




    def read_pdf_PDFMINER(self,pdf_file_path):
        """
        pdf_file_path: 'dir/aaa.pdf'로 구성된 path로부터
        내부의 text 파일을 모두 읽어서 스트링을 리턴함.
        https://pdfminersix.readthedocs.io/en/latest/tutorials/composable.html
        """
        output_string = StringIO()
        with open(pdf_file_path, 'rb') as f:
            parser = PDFParser(f)
            print(parser)

            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
        return str(output_string.getvalue())


if __name__ == "__main__":
    translation('C:/Users/user/Documents/google-trend.pdf')





