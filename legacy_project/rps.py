# cli 기반 게임
import random

def play_game():
    choices = {'가위':0,'바위':1,'보':2}
    user_score = 0
    computer_score = 0
    rounds = 1
    
    print("가위바위보에 오신 것을 환영합니다!")
    
    while True:
        print('\n-------------------------------------------------')
        print(f"라운드 {rounds}")
        print(f"유저 점수: {user_score}, 컴퓨터 점수: {computer_score}")
        
        # User makes a choice
        user_choice = input("선택하세요 (바위, 보, 가위) 또는 게임을 끝내려면 'quit' 입력: ")
        
        if user_choice == 'quit':
            break
        
        if user_choice not in choices:
            print("잘못된 선택입니다. 다시 시도해 주세요.")
            continue
        
        # Computer makes a choice
        computer_choice = random.choice(list(choices.keys()))
        print(f"컴퓨터는 {computer_choice}를 선택했습니다.")
        
        # Determine the winner
        if user_choice == computer_choice:
            print("비겼습니다!")
        elif (user_choice == '가위' and computer_choice == '보') or \
             (user_choice == '바위' and computer_choice == '가위') or \
             (user_choice == '보' and computer_choice == '바위'):
            print("당신이 이겼습니다!")
            user_score += 1
        else:
            print("컴퓨터가 이겼습니다!")
            computer_score += 1
        
        rounds += 1

    print("게임 끝!")
    print(f"최종 점수: 유저 - {user_score}, 컴퓨터 - {computer_score}")

if __name__ == "__main__":
    play_game()
