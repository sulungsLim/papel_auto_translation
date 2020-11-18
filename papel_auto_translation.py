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
import timeit


class translation:

    def __init__(self,path):
        '''
        path : 경로 넣어주자

        '''

        name = path.split("/")[-1]
        paper = self.read_pdf_PDFMINER(path)
        paper = paper.replace("\n","")
        #paper = paper.replace("-

        paper_list = paper.split(".")
        pp = []




        for a in range(len(paper_list)):
            if a % 2 == 0:
                #if paper_list[a][-1] in '0123456789' and paper_list[a + 1][0] in '0123456789':
                #    paper_list[a] = paper_list[a]+'.' + paper_list[a+1]
                #else :
                paper_list[a] = paper_list[a] + '. ' + paper_list[a + 1]
                paper_list[a+1] = ''

        while True:
            try:
                paper_list.remove('')
            except: break

        self.eng_list = []
        self.kor_list = []
        self.double_list = []


        for sentence in paper_list:
            try:

                print(sentence)
                self.translate_eng_kor(sentence)

            except Exception as ex:
                print(ex)
                ex = str(ex)
                if 'Expecting value' in ex:
                    time.sleep(1.5)
                    start_time = timeit.default_timer()
                    while True:
                        try:
                            time.sleep(1.5)
                            self.translate_eng_kor(sentence)
                            break_time = timeit.default_timer()
                            print(" 빠져나오는데 걸린 시간 :",start_time-break_time)

                            break
                        except:
                            pass
                else:
                    pass




        eng_df = pd.DataFrame(self.eng_list)
        kor_df = pd.DataFrame(self.kor_list)
        db_df = pd.DataFrame(self.double_list)
        df_axis1 = pd.concat([eng_df, kor_df], axis=1)  # column bind
        db_df.to_csv('%s_번역한줄씩.txt'%(name),index=False, header=None)
        df_axis1.to_csv('%s_번역병렬.txt'%(name) ,index=False, header=None)

        print(df_axis1)
        print(db_df)

    def translate_eng_kor(self,sentence):
        eng = sentence
        kor = self.kor2eng(sentence)
        self.eng_list.append(eng)
        self.kor_list.append(kor)
        self.double_list.append(eng)
        self.double_list.append(kor)

        print(kor)
        time.sleep(0.5)
        if len(self.eng_list) % 10 == 0:
            time.sleep(1)


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
    translation('C:/Users/user/Documents/attention-is-all-you-need.pdf.pdf')






