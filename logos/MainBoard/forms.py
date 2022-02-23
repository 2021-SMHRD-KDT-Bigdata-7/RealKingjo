from django import forms
from MainBoard.models import life_Answer, life_Question, life_Comment


class life_QuestionForm(forms.ModelForm):
    class Meta:
        model = life_Question  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
        
        labels = {
            'subject': '제목',
            'content': '내용',
        }  
        
        
class life_AnswerForm(forms.ModelForm):
    class Meta:
        model = life_Answer  # 사용할 모델
        fields = [ 'content']  # QuestionForm에서 사용할 Question 모델의 속성
        
        labels = {
            
            'content': '내용',
        }  
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = life_Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }