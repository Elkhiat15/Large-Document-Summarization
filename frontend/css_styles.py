css = '''
<style>
.response {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}

.response.bot {
    background-color: #Ff6347
}

.response .txt {
  color: #000;
  width = 98%;
}
'''

response_template = '''
<div class="response bot">
    <div class="txt"> {{TXT}} </div>
</div>
'''