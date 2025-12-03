# pronunciationChecker 发音检查算法验证
Uses allosaurus, whisper, and deepseek to detect English pronunciation mistakes in an audio clip. Author: Guanyu Ren. 
Please install the necessary packages according to requirements.txt. It's verified to work for python 3.12.
The code uses the MIT license.
使用了allosaurus, whisper库以及deepseek来检查英文音频中的发音错误。作者：任冠羽
请安装requirements.txt中的包，目前已知在python 3.12中可以运行。
代码使用MIT协议。

Here's a sample output:
以下为一个样本输出：

【
根据逐字稿和音标对比，可以推断学生发音可能存在问题的单词如下（忽略语法错误，仅关注发音）：

1. **field trip**  
   - large/medium 识别为 "field trip"，但 base/tiny 识别为 "build trip"，small 识别为 "real trip"。  
   - 音标中对应部分为 `tʰɪŋɪɾskuːlfɹ̩ɾɹ̩tʂɹ̩ðɛntɕʰiːætɹ̩tsɯuətɹɪp`，显示 "field" 可能被模糊发音为类似 "build" 或 "real" 的音。  
   - **可能发音问题**：/f/ 发成 /b/ 或 /r/，或元音 /iː/ 不清晰。

2. **firstly**  
   - 所有模型均识别为 "firstly"，但音标中为 `b̞ɹ̩ɪzɒz`，显示可能将 /fɜːrstli/ 发成类似 "brizoz" 的音。  
   - **可能发音问题**：/f/ 发成 /b/，/ɜːr/ 发成 /ɪ/ 或 /ɒ/，音节重音错误。

3. **characteristics**  
   - large 识别为 "characteristics"，但 medium/small/base/tiny 识别混乱（如 "provides these buildings such characteristics" → "provides the buildings such as a recipe" 等）。  
   - 音标中对应部分为 `hælæəmktsɹ̩nlifɹmajðismulʲiɛz`，显示单词被严重模糊化。  
   - **可能发音问题**：多音节词重音错误、辅音群 /k t r/ 不清晰、元音简化。

4. **sub-stories**  
   - large/medium 识别为 "sub-stories"，但 small/base/tiny 识别为 "child literacy"/"a recipe"/"sub-solving" 等。  
   - 音标中对应部分为 `səbtɑʁi`，显示可能将 "sub-stories" 发成类似 "sub-tari" 的音。  
   - **可能发音问题**：/stɔːriz/ 中的 /ɔːr/ 发成 /ɑ/，/z/ 发音弱化。

5. **understand**  
   - 多数模型识别为 "understand"，但 tiny 识别为 "standard"。  
   - 音标中对应部分为 `b̞əstɛndəz`，显示可能将 /ʌndərˈstænd/ 发成类似 "bəstendəz" 的音。  
   - **可能发音问题**：/ʌ/ 发成 /ə/，/d/ 发成 /t/，重音位置错误。

6. **museum**  
   - 所有模型均识别正确，但音标中为 `mitɑl̪ik̟ʲihæŋoltəŋ̟hiɛm`，显示发音可能模糊，但未影响识别。  
   - **可能发音问题**：/mjuˈziːəm/ 中的 /juː/ 和 /iːəm/ 发音不准确。

7. **clearly**  
   - 多数模型识别为 "clearly"，但音标中为 `klɛɹlinowz`，显示可能将 /ˈklɪrli/ 发成类似 "klerlinowz" 的音。  
   - **可能发音问题**：/ɪ/ 发成 /ɛ/，添加额外音节。

8. **provide**  
   - large/small/base/tiny 中出现 "provide/provides"，但音标中为 `pɹɹ̩vajz`，显示可能将 /prəˈvaɪd/ 发成类似 "prrvajz" 的音。  
   - **可能发音问题**：元音 /ə/ 和 /aɪ/ 不清晰，辅音 /d/ 发成 /z/。

**总结**：学生可能在以下发音方面存在困难：  
- 辅音混淆（如 /f/ 与 /b/、/d/ 与 /t/）。  
- 多音节词重音和元音发音不准确（如 "characteristics"、"understand"）。  
- 单词尾音弱化或错误（如 "stories" 发成 "tari"）。  
- 添加或省略音节（如 "clearly" 发成多音节）。  

建议针对这些单词进行发音练习，特别是辅音清晰度、元音长度和重音模式。
】

The key advantage of this implementation is that the code can detect flaws in one's pronounciation in more detail, and can use natural languages to explain the specfic flaws, making it easier for the end-user to follow and improve.
算法主要优势在于其可以更加细致地检测发音错误，而且可以用自然语言解释问题，让用户更加容易理解。
