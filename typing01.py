import tkinter as tk  
from tkinter import messagebox
import random
import pygame
from PIL import Image, ImageTk  # Pillowをインポート

# --- 問題リスト ---
questions = [
    {"japanese": "犬", "portuguese": "cachorro", "audio": "cachorro.mp3", "image": "cachorro.jpg"},
    {"japanese": "猫", "portuguese": "gato", "audio": "gato.mp3", "image": "gato.jpg"},
    {"japanese": "鳥", "portuguese": "pássaro", "audio": "passaro.mp3", "image": "passaro.jpg"},
    {"japanese": "ありがとう", "portuguese": "obrigado", "audio": "obrigado.mp3", "image": "obrigado.jpg"},
    {"japanese": "こんにちは", "portuguese": "olá", "audio": "ola.mp3", "image": "ola.jpg"}
]

# --- ゲームの状態変数 ---
random.shuffle(questions)  # 問題をシャッフル
current_question_index = 0
score = 0
mistake_count = 0
is_answer_checked = False

# --- Pygameで音声を再生 ---
pygame.mixer.init()

def play_audio(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def play_key_sound():
    pygame.mixer.Sound("keypress.mp3").play()

# --- 問題を表示 ---
def load_question():
    global mistake_count, is_answer_checked
    mistake_count = 0
    is_answer_checked = False
    
    question_label.config(text=f"🔊 {questions[current_question_index]['japanese']}")
    
    # 画像の読み込みと表示
    img_path = questions[current_question_index]['image']
    img = Image.open(img_path)
    img = img.resize((300, 300))  # サイズ調整
    img_tk = ImageTk.PhotoImage(img)
    image_display.config(image=img_tk)
    image_display.image = img_tk  # 参照保持

    # 画像がクリックされた時に音声を再生
    image_display.bind("<Button-1>", lambda event, audio_file=questions[current_question_index]['audio']: play_audio(audio_file))

    play_audio(questions[current_question_index]['audio'])
    
    message_label.config(text="", fg="black")
    answer_input.delete(0, tk.END)
    answer_input.focus()

    submit_button.config(text="回答を送信", command=check_answer)
    reset_button.pack_forget()
    hint_label.config(text="")  

def check_answer(event=None):
    global score, mistake_count, is_answer_checked
    
    if is_answer_checked:
        move_to_next_question()
        return

    user_answer = answer_input.get().strip().lower()
    correct_answer = questions[current_question_index]["portuguese"]

    if user_answer == correct_answer:
        play_audio("seikai.mp3")
        message_label.config(text="🎉 大正解！", fg="green")
        score += 1
        is_answer_checked = True
        hint_label.config(text="")
    else:
        play_audio("hazure.mp3")
        mistake_count += 1
        answer_input.delete(0, tk.END)
        
        if mistake_count >= 3:
            message_label.config(text=f"😢 3回間違えちゃった！正解は: {correct_answer}", fg="red")
            is_answer_checked = True
            hint_label.config(text="")  
        else:
            hint_length = min(mistake_count, len(correct_answer))
            hint = correct_answer[:hint_length] + " " + " ".join("_" * (len(correct_answer) - hint_length))
            hint_label.config(text=f"ヒント: {hint}")

    score_label.config(text=f"スコア: {score}")

    if is_answer_checked:
        if current_question_index == len(questions) - 1:
            submit_button.config(text="終了！", command=end_game)
        else:
            submit_button.config(text="次の問題へ", command=move_to_next_question)

def move_to_next_question():
    global current_question_index
    current_question_index += 1

    if current_question_index < len(questions):
        load_question()
    else:
        end_game()

def end_game():
    messagebox.showinfo("ゲーム終了", f"ゲーム終了！最終スコア: {score}")
    show_reset_button()

def reset_game():
    global current_question_index, score
    current_question_index = 0
    score = 0
    random.shuffle(questions)
    load_question()

def show_reset_button():
    reset_button.pack(pady=20)

root = tk.Tk()
root.title("ブラジルポルトガル語タイピングゲーム")
root.geometry("600x600")  # ウィンドウサイズは元に戻しました
root.configure(bg="white")

question_label = tk.Label(root, text="問題がここに表示されます", font=("Arial", 23), bg="white") #問題の文字の大きさ
question_label.pack(pady=20)

image_display = tk.Label(root, bg="white")
image_display.pack()

answer_input = tk.Entry(root, font=("Arial", 30), justify="center") #回答欄の文字の大きさ
answer_input.pack(pady=10)
answer_input.bind("<Return>", check_answer)

# キー入力音を追加
answer_input.bind("<KeyPress>", lambda event: play_key_sound())

submit_button = tk.Button(root, text="回答を送信", font=("Arial", 18), command=check_answer, bg="#007BFF", fg="white")
submit_button.pack(pady=10)

score_label = tk.Label(root, text="スコア: 0", font=("Arial", 18), bg="white")
score_label.pack()

message_label = tk.Label(root, text="", font=("Arial", 18), bg="white")
message_label.pack()

hint_label = tk.Label(root, text="", font=("Arial", 18), fg="blue", bg="white")
hint_label.pack()

reset_button = tk.Button(root, text="もう一度！", font=("Arial", 18), command=reset_game, bg="#28a745", fg="white")

load_question()
root.mainloop()
