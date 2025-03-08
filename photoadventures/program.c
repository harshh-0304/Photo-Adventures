#include <stdio.h>
void main()
{
    char com[30];
    int i = 2, a = 0;

    printf("\n ENROLLMENT No:21113107010");
    printf("\n Enter comment: ");

    fgets(com, sizeof(com), stdin);

    if (com[0] == '/')
    {
        if (com[1] == '/')
        {
            printf("\n It is a comment");
        }
        else if (com[1] == '*')
        {
            for (i = 2; i < 29; i++)
            {
                if (com[i] == '*' && com[i + 1] == '/')
                {
                    printf("\n It is a comment");
                    a = 1;
                    break;
                }
            }
            if (a == 0)
            {
                printf("\n It is not a comment");
            }
        }
        else
        {
            printf("\n It is not a comment");
        }
    }
    else
    {
        printf("\n It is not a comment");
    }
    getchar();
}
