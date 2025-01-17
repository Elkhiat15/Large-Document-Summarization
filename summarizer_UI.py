import sys
import time
from css_styles import css, response_template
from src import summarize, Doc, Embedding as emb

def run(st, docs, vectors, PdfReader):

       # a boolean variable to check for the first summary output 
       if 'started' not in st.session_state:
              st.session_state.started = False 

       # a boolean variable to check if the Add More button was clicked
       if 'add_more' not in st.session_state:
              st.session_state.add_more = False

       # a boolean variable to check if the Auto Refine button was clicked
       if 'auto_refined' not in st.session_state:
              st.session_state.auto_refined = False

       # a boolean variable to check if the Guided Refine button was clicked
       if 'guided_refined' not in st.session_state:
              st.session_state.guided_refined = False

       # a boolean variable to check if the Add button was clicked
       if 'add' not in st.session_state:
              st.session_state.add = False

       # a string variable to store the last summary output
       if 'response' not in st.session_state:
              st.session_state.response = ""

       # a string variable to store the last summary output
       if 'cum_response' not in st.session_state:
              st.session_state.cum_response = ""

       # a string variable to store the first summary output
       if 'first_response' not in st.session_state:
              st.session_state.first_response = ""

       # the summaries of docs chunks 
       if 'summaries' not in st.session_state:
              st.session_state.summaries = []


       def stream_data(response, t):
              for word in response.split(" "):
                     yield word + " "
                     time.sleep(t)


       def start_summarise():
              if len(docs) < 5:
                     st.warning("The document is too short to be summarized")
              else :
                     with st.spinner("Processing ..."):
                            st.session_state.summaries, st.session_state.response = summarize.summarize(docs, vectors)
                            st.session_state.first_response = st.session_state.response

                     st.write_stream(stream_data(st.session_state.response, 0.03))

             
       def cumulative():
              _, c, _ = st.columns(spec=[1,5,1])
              c.subheader(":blue[Please, Upload Pdf documents that have [5-2000] pages in total.]")

              files = st.file_uploader(label="Cumulative Uploader", accept_multiple_files=True, type="pdf", label_visibility="collapsed")

              process = st.button(label="Add")

              doc = Doc.Document()

              if not files:
                     st.session_state.add = False
                     st.session_state.cum_response = ""
                     
              if process:
                     if not files:
                            st.error("Please, upload Pdf documents")
                     else:
                            total_lenght = 0 
                            exceeded = False
                            for file in files:
                                   pdf_reader = PdfReader(file)
                                   total_lenght+=len(pdf_reader.pages)
                                   if(total_lenght > 2000):
                                          st.warning("Please upload Pdf documents that have less than 2000 pages in total")
                                          exceeded = True
                                          break
                                   doc.extract_data_from_document(pdf_reader)
                            if total_lenght < 5:
                                   st.warning("The document is too short to be summarized")
                            else :
                                   if not exceeded:           
                                          with st.spinner("Processing ..."):
                                                 _, docs2, vectors2 = emb.generate_embedding(False, doc.data)
                                          st.success(f"Processing Done! **{total_lenght}** pages to be added")
                                          with st.spinner("Summarizing ..."):
                                                 st.session_state.cum_response = summarize.get_cumulative_summary(docs2, vectors2, st.session_state.response) 
                                   st.write_stream(stream_data(st.session_state.cum_response, 0.03))
                                   st.session_state.add = True       


 
       def get_refined_summary(with_guide):
              prev_response =  st.session_state.response
              guide = ""
              if with_guide:
                     guide = st.text_input("Enter a Guide to LLM")
                     if guide!="":
                            with st.spinner("Refining ..."):
                                   st.session_state.summaries, st.session_state.response = summarize.summarize(docs, vectors, guide, st.session_state.summaries)
              else :
                     with st.spinner("Refining ..."):
                            st.session_state.response = summarize.refine_summary(prev_response)
    
              if not (guide=="" and with_guide):
                     c1, c2 = st.columns(spec=[1,1], gap="small")
                     with c1.container(border=True):
                            c1.subheader("Previous summary")
                            c1.markdown(response_template.replace(
                                   "{{TXT}}", f"\n\n{prev_response}\n\n"), unsafe_allow_html=True)
                            
                     c2.subheader("Refined Summary")
                     c2.write("\n\n\n")
                     c2.write("\n\n")
                     c2.write_stream(stream_data(st.session_state.response, 0.03))

       st.write(css, unsafe_allow_html=True)
       st.header("Welcome to Summarizer")
       if not st.session_state.started:
              start_summarise()
              st.session_state.started = True 
       else :
              if st.session_state.first_response !="":
                     st.markdown(f"### First response:\n {st.session_state.first_response}")     
 
       c1,c2,c3 = st.columns(spec=[1,1,1])
                     
       if c1.button("Add more books"):
              st.session_state.add_more = True
              st.session_state.auto_refined = False
              st.session_state.guided_refined = False

       if st.session_state.response !="":
              if c2.button("Auto Refine"):
                     st.session_state.auto_refined = True
                     st.session_state.add_more = False
                     st.session_state.guided_refined = False

              if c3.button("Guided Refine"):
                     st.session_state.guided_refined = True
                     st.session_state.add_more = False
                     st.session_state.auto_refined = False

       
       if st.session_state.add_more:
              st.header("Add More Books")
              cumulative()

       if st.session_state.auto_refined:
              st.header("Auto Refine")
              get_refined_summary(with_guide=False)

       if st.session_state.guided_refined:
              st.header("Refine With Guide")
              get_refined_summary(with_guide=True)
